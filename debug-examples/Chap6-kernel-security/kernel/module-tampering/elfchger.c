#include <stdlib.h>
#include <stdio.h>
#include <elf.h>
#include <string.h>
#include <getopt.h>

int ElfGetSectionByName (FILE *fd, Elf32_Ehdr *ehdr, char *section,
                         Elf32_Shdr *shdr);

int ElfGetSectionName (FILE *fd, Elf32_Word sh_name,
                       Elf32_Shdr *shstrtable, char *res, size_t len);

Elf32_Off ElfGetSymbolByName (FILE *fd, Elf32_Shdr *symtab,
                       Elf32_Shdr *strtab, char *name, Elf32_Sym *sym);

void ElfGetSymbolName (FILE *fd, Elf32_Word sym_name,
                       Elf32_Shdr *strtable, char *res, size_t len);

unsigned long ReorderSymbols (FILE *fd, Elf32_Shdr *symtab,
                       Elf32_Shdr *strtab, char *name);

int ReoderRelocation(FILE *fd, Elf32_Shdr *symtab,
                       Elf32_Shdr *strtab, char *name, Elf32_Sym *sym);

int ElfGetSectionByIndex (FILE *fd, Elf32_Ehdr *ehdr, Elf32_Half index,
                          Elf32_Shdr *shdr);

void usage(char *cmd);

int main (int argc, char **argv) {

  FILE *fd;
  Elf32_Ehdr hdr;
  Elf32_Shdr symtab, strtab;
  Elf32_Sym sym;
  Elf32_Off symoffset;
  Elf32_Addr value;

  unsigned long new_index = 0;
  int gflag = 0, vflag = 0, fflag = 0;
  char *sym_name;
  int sym_value = 0;

  long sym_off, str_off;
  int opt;

  if ( argc != 4 && argc != 6 ) {
    usage(argv[0]);
    exit(-1);
  }

  while ((opt = getopt(argc, argv, "vsg")) != -1) {

    switch (opt) {

      case 'g':

        if( argc-1 < optind) {
	    printf("[-] You must specify symbol name!\n");
	    usage(argv[0]);
	    exit(-1);
        }

        gflag = 1;
        sym_name = argv[optind];

        break;

      case 's':

        if( argc-1 < optind) {
          printf("[-] You must specify symbol name!\n");
          usage(argv[0]);
          exit(-1);
        }

        fflag = 1;
        sym_name = argv[optind];

        break;

      case 'v':

        if( argc-1 < optind) {
          printf("[-] You must specify new symbol address\n");
          usage(argv[0]);
          exit(-1);
        }

        vflag = 1;
        sym_value = strtol(argv[optind], (char **) NULL, 16);

        break;

      default:
        usage(argv[0]);
        exit(-1);
    }
  }

  printf("[+] Opening %s file...\n", argv[argc-1]);

  fd = fopen (argv[argc-1], "r+");

  if (fd == NULL) {

    printf("[-] File \"%s\" not found!\n", argv[1]);
    exit(-1);
  }

  printf("[+] Reading Elf header...\n");

  if (fread (&hdr, sizeof (Elf32_Ehdr), 1, fd) < 1) {

    printf("[-] Elf header corrupted!\n");
    exit(-1);
  }

  printf("\t>> Done!\n");

  printf("[+] Finding \".symtab\" section...\n");

  sym_off = ElfGetSectionByName (fd, &hdr, ".symtab", &symtab);

  if (sym_off == -1) {

    printf("[-] Can't get .symtab section\n");
    exit(-1);
  }

  printf("\t>> Found at 0x%x\n", (int )sym_off);
  printf("[+] Finding \".strtab\" section...\n");

  str_off = ElfGetSectionByName (fd, &hdr, ".strtab", &strtab);

  if (str_off  == -1) {

    printf("[-] Can't get .strtab section!\n");
    exit(-1);
  }

  printf("\t>> Found at 0x%x\n", (int )str_off);

  printf("[+] Getting symbol' infos:\n");

  symoffset = ElfGetSymbolByName (fd, &symtab, &strtab, sym_name, &sym);

  if ( (int) symoffset == -1) {

    printf("[-] Symbol \"%s\" not found!\n", sym_name);
    exit(-1);
  }

  if ( gflag == 1 ) {

    if ( ELF32_ST_BIND(sym.st_info) == STB_LOCAL ) {

      unsigned char global;
      unsigned long offset = 0;

      printf("[+] Reordering symbols:\n");

      new_index = ReorderSymbols(fd, &symtab, &strtab, sym_name);

      printf("[+] Updating symbol' infos:\n");

      symoffset = ElfGetSymbolByName(fd, &symtab, &strtab, sym_name, &sym);

      if ( (int) symoffset == -1) {

        printf("[-] Symbol \"%s\" not found!\n", sym_name);
        exit(-1);
      }

      offset = symoffset+1+sizeof(Elf32_Addr)+1+sizeof(Elf32_Word)+2;

      printf("\t>> Replacing flag 'LOCAL' located at 0x%x with 'GLOBAL'\
              \n", (unsigned int)offset);

      if (fseek (fd, offset, SEEK_SET) == -1) {

        perror("[-] fseek: ");
        exit(-1);
      }

      global = ELF32_ST_INFO(STB_GLOBAL, STT_FUNC);

      if (fwrite (&global, sizeof(unsigned char), 1, fd) < 1) {

        perror("[-] fwrite: ");
        exit(-1);
      }

      printf("[+] Updating symtab infos at 0x%x\n", (int )sym_off);

      if ( fseek(fd, sym_off, SEEK_SET) == -1 ) {

        perror("[-] fseek: ");
        exit(-1);
      }

      symtab.sh_info = new_index; // updating sh_info with the new index
                                  // in symbol table.

      if( fwrite(&symtab, sizeof(Elf32_Shdr), 1, fd) < 1 )  {

        perror("[-] fwrite: ");
        exit(-1);
      }

    } else {

      printf("[-] Already global function!\n");
    }

  } else if ( fflag == 1 && vflag == 1 ) {

      memset(&value, 0, sizeof(Elf32_Addr));
      memcpy(&value, &sym_value, sizeof(Elf32_Addr));

      printf("[+] Replacing 0x%.8x with 0x%.8x... ", sym.st_value, value);

      if (fseek (fd, symoffset+sizeof(Elf32_Word), SEEK_SET) == -1) {

        perror("[-] fseek: ");
        exit(-1);
      }

      if (fwrite (&value, sizeof(Elf32_Addr), 1, fd) < 1 )  {

        perror("[-] fwrite: ");
        exit(-1);
      }

      printf("done!\n");

      fclose (fd);
}

return 0;
}

/* This function returns the offset relative to the symbol name "name" */

Elf32_Off ElfGetSymbolByName(FILE *fd, Elf32_Shdr *symtab,
        Elf32_Shdr *strtab, char *name, Elf32_Sym *sym) {

  unsigned int i;
  char symname[255];

  for ( i = 0; i < (symtab->sh_size/symtab->sh_entsize); i++) {

    if (fseek (fd, symtab->sh_offset + (i * symtab->sh_entsize),
               SEEK_SET) == -1) {

      perror("\t[-] fseek: ");
      exit(-1);
    }

    if (fread (sym, sizeof (Elf32_Sym), 1, fd) < 1) {

      perror("\t[-] read: ");
      exit(-1);
    }

    memset (symname, 0, sizeof (symname));

    ElfGetSymbolName (fd, sym->st_name, strtab, symname, sizeof (symname));

    if (!strcmp (symname, name)) {

      printf("\t>> Symbol found at 0x%x\n",
                    symtab->sh_offset + (i * symtab->sh_entsize));

      printf("\t>> Index in symbol table: 0x%x\n", i);

      return symtab->sh_offset + (i * symtab->sh_entsize);
    }
  }

  return -1;
}

/* This function returns the new index of symbol "name" inside the symbol
 * table after re-ordering. */

unsigned long ReorderSymbols (FILE *fd, Elf32_Shdr *symtab,
              Elf32_Shdr *strtab, char *name) {

  unsigned int i = 0, j = 0;
  char symname[255];
  Elf32_Sym *all;
  Elf32_Sym temp;
  unsigned long new_index = 0;
  unsigned long my_off = 0;

  printf("\t>> Starting:\n");

  all = (Elf32_Sym *) malloc(sizeof(Elf32_Sym) *
                      (symtab->sh_size/symtab->sh_entsize));

  if ( all == NULL ) {

    return -1;

  }

  memset(all, 0, symtab->sh_size/symtab->sh_entsize);

  my_off = symtab->sh_offset;

  for ( i = 0; i < (symtab->sh_size/symtab->sh_entsize); i++) {

    if (fseek (fd, symtab->sh_offset + (i * symtab->sh_entsize),
							 SEEK_SET) == -1) {

      perror("\t[-] fseek: ");
      exit(-1);
    }

    if (fread (&all[i], sizeof (Elf32_Sym), 1, fd) < 1) {

      printf("\t[-] fread: ");
      exit(-1);
    }

    memset (symname, 0, sizeof (symname));

    ElfGetSymbolName(fd, all[i].st_name, strtab, symname, sizeof(symname));

    if (!strcmp (symname, name)) {

      j = i;

      continue;
    }
  }

  temp = all[j];

  for ( i = j; i < (symtab->sh_size/symtab->sh_entsize); i++ ) {

    if ( i+1 >= symtab->sh_size/symtab->sh_entsize )
      break;

    if ( ELF32_ST_BIND(all[i+1].st_info) == STB_LOCAL ) {

      printf("\t>> Moving symbol from %x to %x\n", i+1, i);

      all[i] = all[i+1];

    } else {

      new_index = i;

      printf("\t>> Moving our symbol from %d to %x\n", j, i);

      all[i] = temp;
      break;
    }
  }

  printf("\t>> Last LOCAL symbol: 0x%x\n", (unsigned int)new_index);

  if ( fseek (fd, my_off, SEEK_SET) == -1 ) {

      perror("\t[-] fseek: ");
      exit(-1);
  }

  if ( fwrite(all, sizeof( Elf32_Sym), symtab->sh_size/symtab->sh_entsize,
              fd) < (symtab->sh_size/symtab->sh_entsize )) {

      perror("\t[-] fwrite: ");
      exit(-1);
  }

  printf("\t>> Done!\n");

  free(all);

  return new_index;
}


int ElfGetSectionByIndex (FILE *fd, Elf32_Ehdr *ehdr, Elf32_Half index,
                          Elf32_Shdr *shdr) {

  if (fseek (fd, ehdr->e_shoff + (index * ehdr->e_shentsize),
             SEEK_SET) == -1) {

    perror("\t[-] fseek: ");
    exit(-1);
  }

  if (fread (shdr, sizeof (Elf32_Shdr), 1, fd) < 1) {

    printf("\t[-] Sections header corrupted");
    exit(-1);
  }

  return 0;
}


int ElfGetSectionByName (FILE *fd, Elf32_Ehdr *ehdr, char *section,
                         Elf32_Shdr *shdr) {

  int i;
  char name[255];
  Elf32_Shdr shstrtable;

  ElfGetSectionByIndex (fd, ehdr, ehdr->e_shstrndx, &shstrtable);

  memset (name, 0, sizeof (name));

  for ( i = 0; i < ehdr->e_shnum; i++) {

    if (fseek (fd, ehdr->e_shoff + (i * ehdr->e_shentsize),
               SEEK_SET) == -1) {

      perror("\t[-] fseek: ");
      exit(-1);
    }

    if (fread (shdr, sizeof (Elf32_Shdr), 1, fd) < 1) {

      printf("[-] Sections header corrupted");
      exit(-1);
    }

    ElfGetSectionName (fd, shdr->sh_name, &shstrtable,
                       name, sizeof (name));

    if (!strcmp (name, section)) {

      return ehdr->e_shoff + (i * ehdr->e_shentsize);

    }
  }

  return -1;
}

int ElfGetSectionName (FILE *fd, Elf32_Word sh_name,
                       Elf32_Shdr *shstrtable, char *res, size_t len) {

  size_t i = 0;

  if (fseek (fd, shstrtable->sh_offset + sh_name, SEEK_SET) == -1) {

    perror("\t[-] fseek: ");
    exit(-1);
  }

  while ( (i < len-1) || *res != '\0' ) {

    *res = fgetc (fd);
    i++;
    res++;

  }

  return 0;
}


void ElfGetSymbolName (FILE *fd, Elf32_Word sym_name,
                       Elf32_Shdr *strtable, char *res, size_t len)
{
  size_t i = 0;

  if (fseek (fd, strtable->sh_offset + sym_name, SEEK_SET) == -1) {

    perror("\t[-] fseek: ");
    exit(-1);
  }

  while ((i < len-1) || *res != '\0') {

    *res = fgetc (fd);
    i++;
    res++;

  }

  return;
}

void usage(char *cmd) {

  printf("Usage: %s <option(s)> <module_name>\n", cmd);
  printf("Option(s):\n");
  printf(" -g [symbol]\tSymbol we want to change the binding as global\n");
  printf("Or:\n");
  printf(" -s [symbol]\tSymbol we want to change the value (address)\n");
  printf(" -v [value] \tNew value (address) for symbol\n");

  return;
}


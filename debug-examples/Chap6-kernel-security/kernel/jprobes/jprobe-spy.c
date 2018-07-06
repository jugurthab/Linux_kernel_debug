#include<linux/module.h>
#include<linux/kernel.h>
#include<linux/init.h>
#include<linux/kprobes.h>
#include <linux/uaccess.h>

#define KERNEL_STATIC_ALLOC_FILENAME_LENGTH 60

MODULE_AUTHOR("Jugurtha BELKALEM");
MODULE_DESCRIPTION("Basic example of Jprobes");
MODULE_LICENSE("GPL");

static long snoop_do_sys_open(int dfd, const char __user *filename, int flags, umode_t mode){
    char tmp[KERNEL_STATIC_ALLOC_FILENAME_LENGTH];
    // Copies filename from userspace to kernel buffer
    copy_from_user(tmp, filename, KERNEL_STATIC_ALLOC_FILENAME_LENGTH-1);
    // displays do_sys_open arguments
    printk("jprobe spy : dfd = 0x%x, filename = %s flags = 0x%x mode umode %x\n", dfd, tmp, flags, mode);
  
    jprobe_return();
}
 
static struct jprobe my_probe;
 
static int myinit(void)
{
    my_probe.kp.addr = (kprobe_opcode_t *)0xffffffffa2c433e0;
    my_probe.entry = (kprobe_opcode_t *)snoop_do_sys_open;
    register_jprobe(&my_probe);
    return 0;
}
 
static void myexit(void)
{
    unregister_jprobe(&my_probe);
    printk("module removed\n ");
}
 
module_init(myinit);
module_exit(myexit); 

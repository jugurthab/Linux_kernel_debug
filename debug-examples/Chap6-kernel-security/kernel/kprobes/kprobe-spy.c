#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/version.h>
#include <linux/kprobes.h>

MODULE_AUTHOR("Jugurtha BELKALEM");
MODULE_DESCRIPTION("Basic example of Kprobes");
MODULE_LICENSE("GPL");


static int Pre_Handler(struct kprobe *p, struct pt_regs *regs){
    printk("-------- Pre_Handler Code addr => 0x%p-----\n",p->addr);
    
   
    printk("ax=%ld, bx=%ld, cx=%ld, dx=%ld, ip=%ld, cs=%ld, sp=%ld, ss=%ld",regs->ax, regs->bx, regs->cx, regs->dx, regs->ip, regs->cs, regs->sp, regs->ss);   

    
    return 0;
}

void Post_Handler(struct kprobe *p, struct pt_regs *regs, unsigned long flags){
    printk("--------- Post_Handler --------- ");
    regs->ax = 0; regs->bx = 0; regs->cx = 0; regs->dx = 0;
    regs->ip = 0; regs->cs = 0; regs->sp = 0; regs->ss = 0;


    printk("ax=%ld, bx=%ld, cx=%ld, dx=%ld, ip=%ld, cs=%ld, sp=%ld, ss=%ld",regs->ax, regs->bx, regs->cx, regs->dx, regs->ip, regs->cs, regs->sp, regs->ss);
}
static struct kprobe kp;
static int __init intializeModule(void)
{
    printk(KERN_DEBUG "Module is running !\n");
       
    kp.pre_handler = Pre_Handler;
    kp.post_handler = Post_Handler;
    kp.addr = (kprobe_opcode_t *) 0xffffffffb00433e0; // do_sys_open
    register_kprobe(&kp);
    return 0;
}

static void __exit cleanUpModule(void)
{
    unregister_kprobe(&kp);
    printk(KERN_DEBUG "Module has been removed!\n");
}

module_init(intializeModule);
module_exit(cleanUpModule);

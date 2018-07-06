
#include <linux/module.h>
#include <linux/init.h>

static int fake_init(void) __attribute__((used));
 static int fake_init(void){
    printk(KERN_DEBUG "Hacking is great!\n");
    return 0;
}


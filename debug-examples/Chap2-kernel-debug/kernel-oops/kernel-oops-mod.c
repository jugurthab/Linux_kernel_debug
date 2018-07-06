#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static void createOops(void){
	*(int *)0 =0;
}

static int __init initializeModule(void){
	printk("Hey SMILE!This is a kernel oops test module!!!\n");				
	createOops();		
	return 0;
}

static void __exit cleanModule(void){
	printk("Goodby SMILE! Module exited!\n");
}

module_init(initializeModule);
module_exit(cleanModule);


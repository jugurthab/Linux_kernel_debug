#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
MODULE_AUTHOR("Jugurtha BELKALEM");
MODULE_DESCRIPTION("Basic example of character driver");
MODULE_LICENSE("GPL");

int major;

static ssize_t basic_read_function(struct file *file, char *buf, size_t count, loff_t *ppos)
{
    printk(KERN_DEBUG "read() function executed\n");
    return 0;
}

static ssize_t basic_write_function(struct file *file, const char *buf, size_t count, loff_t *ppos)
{
    printk(KERN_DEBUG "write() function executed\n");
    return 0;
}

static int basic_open_function(struct inode *inode, struct file *file)
{
    printk(KERN_DEBUG "open() function executed\n");
    return 0;
}

static int basic_release_function(struct inode *inode, struct file *file)
{
    printk(KERN_DEBUG "close() function executed\n");
    return 0;
}

static struct file_operations fops = 
{
    read : basic_read_function,
    write : basic_write_function,
    open : basic_open_function,
    release : basic_release_function
};


static int __init intializeModule(void)
{

    major = register_chrdev(0, "basictestdriver", &fops);
    
    if(major < 0)
    {
        printk(KERN_WARNING "Cannot allocate device with provided major number\n");
        return 1;
    }
    
    printk(KERN_DEBUG "Module is running major %d !\n", major);
    return 0;
}

static void __exit cleanUpModule(void)
{
    unregister_chrdev(major, "basictestdriver"); 
    printk(KERN_DEBUG "Module has been removed!\n");
}

module_init(intializeModule);
module_exit(cleanUpModule);

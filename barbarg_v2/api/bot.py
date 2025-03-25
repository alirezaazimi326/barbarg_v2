import frappe
import subprocess

@frappe.whitelist()
def start_bot():
    try:
        # Update all records in Drivers Log
        frappe.db.sql("""
            UPDATE `tabDrivers Log` 
            SET situation = 'Pending', status = NULL, time_taken = NULL
        """)
        frappe.db.commit()

        frappe.logger().info("Updated Drivers Log before starting the bot.")

        # Path to the directory containing your bot
        bot_directory = "/home/frappe/Barbarg-Ubuntu"

        # Command to activate the environment and run main.py
        command = f"cd {bot_directory} && . env/bin/activate && python main.py"

        # Run the command in a new process
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Log the process ID for later management
        frappe.logger().info(f"Bot started with PID: {process.pid}")

        return {"message": "Bot started successfully", "pid": process.pid}
    
    except Exception as e:
        frappe.logger().error(f"Failed to start bot: {str(e)}")
        return {"message": f"Failed to start bot: {str(e)}"}

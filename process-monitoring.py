import psutil, os, time 

class Process:	

	def __init__(self,pid_value):
		"""Constructor based on the PID"""
		self.pid_value=pid_value 
		self.process = psutil.Process(pid=self.pid_value)

	def get_number_of_files(self):
		"""Gets the number of opened files descriptor at the same time"""
		return self.process.get_num_fds() 

	def get_dump_memory_of_server(self):
		"""Get the memory used by the server/system in bytes and kbytes"""
		server_dump_memory_usage = psutil.virtual_memory().used 
		server_dump_memory_usage_kb = server_dump_memory_usage/1024
		return server_dump_memory_usage_kb
	
	def get_dump_memory_of_demon(self):
		"""Gets the memory used by the demon in bytes and Mbytes"""
		demon_dump_memory_usage = self.process.get_memory_info().vms
		demon_dump_memory_usage_mb = demon_dump_memory_usage/(1024**2)
		return demon_dump_memory_usage_mb 

	def get_the_memory_load_of_the_system(self):
		"""Gets the memory load of the system"""	
		percentMEM = psutil.virtual_memory().percent
		return percentMEM 

	def get_the_cpu_load_of_the_system(self):
		"""Gets the cpu load of the system"""		
		percentCPU = psutil.cpu_percent()
		return percentCPU

	def get_list_of_all_opened_files(self):
		"""Gets the list of all opened files descriptors"""
		list_of_files=[]
		ls_result = os.popen('ls -l /proc/'+str(self.pid_value)+'/fd')
		ls_result_read = ls_result.readlines()
		for i in range (1,self.get_number_of_files()):
			list_of_files.append(ls_result_read[i].split(' ').pop().rstrip())
		return list_of_files 

	def get_a_core(self):
		"""Gets a dumpcore file"""
		print ""
		print "Generation of a dumpcore for the pid number " + str(self.pid_value) +" ..."
		os.system("sudo gcore "+ str(self.pid_value) +" > log_core_"+ str(self.pid_value) +".txt 2>&1")
		print "...Done"
		print ""

	def get_children_list_requiring_alert(self):
		"""Gets a list of children on which the alert has to be applied"""
		children_list_with_alert=[]
		if self.process.get_children() is not None: 
			for i in self.process.get_children():
				if i.get_num_fds()>100:
					children_list_with_alert.append(i)
		return children_list_with_alert			


	def print_alert(self):

		print ""
		print ""
		print "------------------------------------------------------------------------------------------------------"
		print " Alert : The number of files opened by the process " + str(self.pid_value) + " is " + str(process.get_number_of_files()) + " which is above 100  "
		print "------------------------------------------------------------------------------------------------------"
		print ""
		print "The dump memory usage of the server is (top-like)       :  " + str(process.get_dump_memory_of_server()) + ' Kb'
		print "The dump memory usage of the demon is  (top-like)       :  " + str(process.get_dump_memory_of_demon()) + '  Mb'
		print "The memory load of the system is                        :  " + str(process.get_the_memory_load_of_the_system()) + " %"
		print "The cpu load of the system is                           :  " + str(process.get_the_cpu_load_of_the_system()) + " %"
		print ""
		print ""
		print "The list of all opened files is : \n \n " + str(process.get_list_of_all_opened_files())
		print ""
		print "" 	


if __name__ == '__main__':

	# Gets the PID from the user 

	pid=input("Enter the PID of the process to monitor : ")
	process=Process(pid)

	# Starts the monitoring of this process and its children 

	while psutil.pid_exists(pid)==True:
		number_of_files_opened=process.get_number_of_files()
		if number_of_files_opened>100: 
			process.print_alert()
			process.get_a_core()
			if process.get_children_list_requiring_alert() is not None:
				for i in process.get_children_list_requiring_alert():
					child_pid=int(str(i).split("=",2)[1].split(",")[0])  
					child_process=Process(child_pid)
					child_process.get_a_core()
		time.sleep(3)			

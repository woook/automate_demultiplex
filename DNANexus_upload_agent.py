'''
Created on 21 Sep 2016

Once demultiplexing has been complete the files require uploading to DNANexus.

This script will be scheduled to run and identify any folders that have not been uploaded.

It will trigger the upload agent to upload into the required project
 
@author: aled
'''

import os
import subprocess
import datetime
import smtplib
from email.Message import Message
import fnmatch


class get_list_of_runs():
    '''Loop through the directories in the directory containing the runfolders'''
    
    def __init__(self):
        # directory of run folders - must be same as in upload2Nexus()
        self.runfolders = "/media/data1/share" # workstation
        #self.runfolders = "/home/aled/demultiplex_testing" # aledpc
        #self.runfolders = "/media/data2/data" # workstation dummy
        self.now=""
    
    def loop_through_runs(self):
        #set a time stamp to name the log file
        self.now = str('{:%Y%m%d_%H}'.format(datetime.datetime.now()))
        # create a list of all the folders in the runfolders directory
        all_runfolders = os.listdir(self.runfolders)
        #print all_runfolders
        upload=upload2Nexus()
        # for each folder if it is not samplesheets pass the runfolder to the next class
        for folder in all_runfolders:
            if folder != "samplesheets":
                if folder.endswith('.gz'):
                    pass
                else:
                    upload.already_uploaded(folder, self.now)

        self.combine_log_files()

    def combine_log_files(self):
        # count number of log files that match the time stamp
        count=0
        # empty list
        list_of_logfiles=[]
        #loop through the folder containing log files
        for file in os.listdir(upload2Nexus().DNA_Nexus_workflow_logfolder):
            #if is one with this time stamp, ie if was made by this running of this script
            if fnmatch.fnmatch(file,self.now+'*'):
                #add count and append to list
                count=count+1
                list_of_logfiles.append(upload2Nexus().DNA_Nexus_workflow_logfolder+file)
        
        #if more than one log file we want to concatenate them
        if count > 1:
            # get the filename with the longest name
            longest_name=max(list_of_logfiles, key=len)
            #remove from the list
            list_of_logfiles.remove(longest_name)
            #concatenate all the remaining filenames into a string, seperated by spaces
            remaining_files=" ".join(list_of_logfiles)

            # combine all into one file with the longest filename (that will have the run folder name)
            cmd = "cat " + remaining_files + " >> " + longest_name
            # remove the files that have been written to the longer file
            rmcmd= "rm " + remaining_files
            
            # run the command, redirecting stderror to stdout
            proc = subprocess.call([cmd], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            proc = subprocess.call([rmcmd], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)


class upload2Nexus():
    ''' This class is fed a runfolder which may be ready to be uploaded to DNA Nexus''' 
    
    def __init__(self):
        # directory of run folders - must be same as in get_list_of_runs()
        self.runfolders = "/media/data1/share" # workstation
        #self.runfolders = "/media/data2/data" # workstation dummy
        #self.runfolders = "/home/aled/demultiplex_testing" # aledpc
        
        # file which denotes demultiplexing is underway/complete 
        self.demultiplexed = "demultiplexlog.txt"
        
        # set empty variables to be defined based on the run  
        self.runfolder = ""
        self.runfolderpath = ""

        #succesful run statement
        self.logfile_success = "Processing completed with 0 errors and 0 warnings."
        
        # upload started log file
        self.upload_started_file = "DNANexus_upload_started.txt"
        
        # upload agent
        self.upload_agent = "/home/mokaguys/Documents/apps/dnanexus-upload-agent-1.5.17-linux/ua"
        
        # fastq folder
        self.fastq_folder = "Data/Intensities/BaseCalls"
        self.fastq_folder_path = ""
        
        #upload_agent_logfile
        self.upload_agent_logfile = "/home/mokaguys/Documents/automate_demultiplexing_logfiles/Upload_agent_log/"
        self.upload_agent_logfile_name=""
        

        # DNA Nexus run command log file
        self.DNA_Nexus_workflow_logfolder = "/home/mokaguys/Documents/automate_demultiplexing_logfiles/DNA_Nexus_workflow_logs/"

        # string of fastqs for upload agent
        self.fastq_string = ""
        # list of fastqs to get ngs run number and WES batch
        self.list_of_samples = []

        #strings for NGSrun and wes numbers
        self.NGS_run = ''
        self.wes_number = ''
        
        # variables for running pipeline
        self.bash_script=""
        self.source_command = "#!/bin/bash\n. /etc/profile.d/dnanexus.environment.sh\ndx select NGS_runs\n"
        self.base_command = "jobid=$(dx run apps/GATK3.5_160918 -y" # GATK3.5_160918
        self.arg1 = " -istage-Bz3YpP80jy1Y1pZKbZ35Bp0x.reads=" # GATK3.5_160918
        self.arg2 = " -istage-Bz3YpP80jy1x7G5QfG3442gX.reads=" # GATK3.5_160918
        self.arg3 = " -istage-Byz9BJ80jy1k2VB9xVXBp0Fg.reads_fastqgz=" # GATK3.5_160918
        self.arg4 = " -istage-Byz9BJ80jy1k2VB9xVXBp0Fg.reads2_fastqgz=" # GATK3.5_160918
        #self.base_command = "jobid=$(dx run apps/GATK3.5_Aled -y" # GATK3.5_Aled
        #self.arg1 = " -istage-F04G1Gj0F1V1Jvg78Q33z62q.reads=" # GATK3.5_Aled
        #self.arg2 = " -istage-F04G1K00F1V3jfk2F435ZVP2.reads=" # GATK3.5_Aled
        #self.arg3 = " -istage-F04G1Pj0F1V5zxZFvxkJfx0b.reads_fastqgz=" # GATK3.5_Aled
        #self.arg4 = " -istage-F04G1Pj0F1V5zxZFvxkJfx0b.reads2_fastqgz=" # GATK3.5_Aled
        self.arg5 = " --dest="
        self.arg6 = " --yes --brief)"
        #argument to capture jobids
        self.depends_list="depends_list += \" --depends-on \"$jobid"
        self.dx_run = []

        #create path to data in nexus eg /runfolder/Data
        self.nexus_path = ""
        
        #email server settings
        self.user = 'AKIAIO3XY2MMSBEQNNXQ'
        self.pw   = '***REMOVED***'
        self.host = 'email-smtp.eu-west-1.amazonaws.com'
        self.port = 587
        self.me   = 'gst-tr.mokaguys@nhs.net'
        self.you  = ('gst-tr.mokaguys@nhs.net',)
        self.smtp_do_tls = True
        
        # email message
        self.email_subject = ""
        self.email_message = ""
        self.email_priority = 3

        #variable to rename log file.
        self.rename=""
        self.now=""

    def already_uploaded(self, runfolder, now):
        '''check folder hasn't already been uploaded'''
        self.now=now
		#open the logfile for this hour's cron job.
        self.upload_agent_logfile_name=self.upload_agent_logfile+self.now+"_"+self.rename+".txt"
        self.upload_agent_script_logfile = open(self.upload_agent_logfile_name,'a')

        # capture the runfolder 
        self.runfolder = str(runfolder)
               
        # create full path to runfolder
        self.runfolderpath = self.runfolders + "/" + self.runfolder
       
        self.upload_agent_script_logfile.write("\n----------------------" + str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())) + "-----------------\nAssessing......... " + self.runfolderpath + "\n")
        print "looking at runfolder "+runfolder
         
        #look for the file denoting the upload has started
        if os.path.isfile(self.runfolderpath + "/" + self.upload_started_file):
            self.upload_agent_script_logfile.write("self.upload_started_file present \n---STOP---\n")
        else:
            #if not check demultiplex has finished succesfully and write to file
            print "not already uploaded"
            self.upload_agent_script_logfile.write("self.upload_started_file_not_present so continue\n")
            self.demultiplex_completed_successfully() 
        
    def demultiplex_completed_successfully(self):
        '''check if the demultiplexing finished successfully by reading the last line of the demultiplex log'''
        
        #check demultiplexing has actually been done
        if os.path.isfile(self.runfolders + "/" + self.runfolder + "/" + self.demultiplexed):
            #open log file
            logfile = open(self.runfolders + "/" + self.runfolder + "/" + self.demultiplexed,'r')
            
            #find the last line of the demultiplexing log file
            lastline = ""
            for i in logfile:
                lastline = i
            print lastline
            # check if the success statement is in the last line
            if  self.logfile_success in lastline:
                self.upload_agent_script_logfile.write("demultiplex was successfully completed. compile a list of fastqs \n")
                print "successfully demultiplexed"
                # if successfull call the module which creates a list of fastqs  
                self.find_fastqs()
            else:
            	#write to logfile that demultplex was not successful
                self.upload_agent_script_logfile.write("demultiplex was NOT successfully completed. \n ---STOP---\n")
        else:
        	# write to logfile that not yet demultiplexed
            self.upload_agent_script_logfile.write("demultiplex has not been performed.\n---STOP---\n")
            
    def find_fastqs(self):
        ''' find all the fastqs and send them to the upload command'''
        
        # folder containing the fastqs for this project
        self.fastq_folder_path = self.runfolderpath + "/" + self.fastq_folder
        
        # create a list of all files within the fastq folder
        all_fastqs = os.listdir(self.fastq_folder_path)
        
            
        # find all fastqs
        for fastq in all_fastqs:
            if fastq.endswith('fastq.gz'):
                # select WES samples only
                if "WES" in fastq:
                    #exclude undertermined samples 
                    if fastq.startswith('Undetermined'):
                        pass
                    else:
                        #build the list of fastqs with full file paths
                        self.fastq_string = self.fastq_string + " " + self.fastq_folder_path + "/" + fastq
                        #add the fastq name to a list to be used in create_nexus_file_path
                        self.list_of_samples.append(fastq)
                    
        #write to logfile
        self.upload_agent_script_logfile.write("list of fastqs found\n")
        
        #build the file path with WES batch and NGS run numbers
        self.create_nexus_file_path()
        
        # send list to module to trigger upload
        self.upload()       
    
    def create_nexus_file_path(self):
        ''' get info from the fastq names to have a more informative folder structure within DNA nexus 
        want the ngs run number eg NGS95a and any wes batches eg WES_5
        example fastq name = NGS95a_13_94947_SW_WES_5_S8_R2_001.fastq.gz'''
        
        # a list to hold all the wes numbers
        WES_numbers = []
        # for each fastq in the list of fastqs
        for fastq in self.list_of_samples:
            # split on underscores to capture the first element which is the ngs number
            splitfastq = fastq.split("_")
            # assign self.ngs_run
            self.ngs_run = splitfastq[0]
            
            # if the run has any WES samples
            if "WES" in fastq:
                # split on _WES to split the fastq name into two
                splitfastq = fastq.split("_WES")
                # take the second half of it and split on "_S"
                splitfastq2 = splitfastq[1].split("_S")

                #This should split the string in half again, with the first element either _5 or 5 depending if tit's WES_5 or WES5
                #append this to WES (which was replaced as part of the split) and add to a list
                wesrun = "WES" + splitfastq2[0].replace('_','')
                WES_numbers.append(wesrun)
        
        # create a list of unique WES batches
        for wesnumber in set(WES_numbers):
            # if multiple WES batches append each one with an underscore
            if len(self.wes_number) > 1:
                self.wes_number = self.wes_number + "_" + wesnumber
            else:
                self.wes_number = wesnumber

        # self.nexus path
        self.nexus_path = self.runfolder + "_" + self.ngs_run + "_" + self.wes_number + "/Data/Intensities/BaseCalls"
        print self.nexus_path


    def upload(self):
        '''takes a list of all the fastqs (with full paths) and calls the upload agent.'''
		
        # perform upload agent test
        self.test_upload_agent()

		# build the nexus upload command                        
        nexus_upload_command = self.upload_agent + " --auth-token A3TJlJ3Pb19ZYPlgDCdRE2ZsM2UN3ydH --project NGS_runs --folder /" + self.nexus_path + " --do-not-compress --upload-threads 10" + self.fastq_string
        
        #write to logfile
        self.upload_agent_script_logfile.write("Nexus command = \n" + nexus_upload_command + "\n")
        
        #create file to show demultiplexing has started
        upload_started = open(self.runfolderpath + "/" + self.upload_started_file, 'w')
        
        # run the command, redirecting stderror to stdout
        proc = subprocess.Popen([nexus_upload_command], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
         
        # capture the streams (err is redirected to out above)
        (out, err) = proc.communicate()
        
        #write to log
        upload_started.write("\n----------------------"+str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))+"-----------------\n" + out)
        upload_started.close()
        
        # set email content
        self.email_subject = "MOKAPIPE ALERT: Upload of " + self.runfolder + " completed"
        self.email_priority = 3
        self.email_message = self.runfolder + " \t has been uploaded to DNA Nexus :-)\nPlease see log file at: " + self.runfolderpath + "/" + self.upload_started_file
        # send email
        self.send_an_email()
        # start pipeline
        self.create_run_pipeline_command()

        # close the log file
        self.upload_agent_script_logfile.close()

        #rename file to show what runs were affected.
        self.rename=self.rename+self.runfolder
        os.rename(self.upload_agent_logfile_name,self.upload_agent_logfile_name.replace('.txt','')+self.rename+".txt")
        

    def send_an_email(self):
        #body = self.runfolder
        self.upload_agent_script_logfile.write("Sending email to...... " + str(self.you))
        #msg  = 'Subject: %s\n\n%s' % (self.email_subject, self.email_message)
        m = Message()
        #m['From'] = self.me
        #m['To'] = self.you
        m['X-Priority'] = str(self.email_priority)
        m['Subject'] = self.email_subject
        m.set_payload(self.email_message)
        
        
        server = smtplib.SMTP(host = self.host,port = self.port,timeout = 10)
        server.set_debuglevel(10)
        server.starttls()
        server.ehlo()
        server.login(self.user, self.pw)
        server.sendmail(self.me, [self.you], m.as_string())

        #write to logfile
        self.upload_agent_script_logfile.write("Email sent\n")
        #self.upload_agent_script_logfile.close()

    def test_upload_agent(self):
        '''test the upload agent is installed'''
        
        #command
        command = self.upload_agent + " --version"

        # run the command
        proc = subprocess.Popen([command], stderr = subprocess.PIPE, stdout = subprocess.PIPE, shell = True)
        
        # capture the streams
        (out, err) = proc.communicate()
        
        if "Upload Agent Version:" not in out:
            self.email_subject = "MOKAPIPE ALERT: ERROR - PRESENCE OF DNA NEXUS UPLOAD AGENT TEST FAILED"
            self.email_priority = 1
            self.email_message = "The test to check the upload agent has been installed (" + command + ") failed"
            self.send_an_email()
            raise Exception, "Upload agent not installed"

        # write this to the log file
        self.upload_agent_script_logfile.write("upload agent check passed\n")

    def  create_run_pipeline_command(self):
        '''loop through the list of fastqs to create a set of commands to initiate the pipeline'''
        self.bash_script=self.DNA_Nexus_workflow_logfolder + self.runfolder + ".sh"
        
        #open bash script
        self.DNA_Nexus_bash_script = open(self.bash_script, 'w')
        #write command to log file
        self.DNA_Nexus_bash_script.write(self.source_command)

        #loop through list of fastq files
        for fastq in self.list_of_samples:
            #take read one
            if "_R1_" in fastq:
                #assign read1
                read1 = self.nexus_path+"/"+fastq
                # assign read2 by replacing R1 with R2
                read2 = self.nexus_path+"/"+fastq.replace("_R1_", "_R2_")
                # create the dx command
                command = self.base_command + self.arg1 + read1 + self.arg2 + read2 + self.arg3 + read1 + self.arg4 + read2 + self.arg5 + self.runfolder + "_" + self.ngs_run + "_" + self.wes_number + self.arg6
                #add command for each pair of fastqs to a list 
                self.dx_run.append(command)
        
                
        
        # call module to issue the dx run commands
        self.run_pipeline()

        #record timestamp
        self.DNA_Nexus_bash_script = open(self.bash_script, 'a')
        self.DNA_Nexus_bash_script.write("----------------------" + str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())) + "-----------------\n")
        self.DNA_Nexus_bash_script.close()

    def run_pipeline(self):
        '''issue dna nexus run commands''' 
               
        # loop through all dx_run commands:       
        for command in self.dx_run:
            # write command to log file
            self.DNA_Nexus_bash_script.write(command+"\n")
            # write line to append job id to depends_list
            self.DNA_Nexus_bash_script.write(self.depends_list+"\n")

            # capture the sample name
            #step 1 split the command to get the last argument (read2)
            split_command = command.split(self.arg4)
            read_2 = split_command[1].replace(self.nexus_path,'')

            # split this fastq name on _S1_ and take first half to get sample name
            read = read_2.split("_")

            sample = read[0]+"_"+read[1]+"_"+read[2]+"_"+read[3]+"_"+read[4]
            
            #capture the workflow used
            # split command on -y 
            split_command=command.split('-y')
            # take first bit and remove dx run 
            app=split_command[0].replace("dx run apps/",'').replace(self.source_command,"")


        # issue multiqc command
        #self.DNA_Nexus_bash_script.write(command+"\n")
       	#self.DNA_Nexus_bash_script.write("\#multiqc command $depends_list")
        
        #close bash script file handle
        self.DNA_Nexus_bash_script.close()

        #write to cron job script
       	self.upload_agent_script_logfile.write("dx run commands issued\nSee "+self.bash_script+"\n")
        
        # # run a command to execute the bash script made above
        cmd="bash "+self.bash_script
        proc = subprocess.Popen([cmd], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        
        # capture the streams
        (out, err) = proc.communicate()
        print err 
        print out

        #create email message
        self.email_subject = "MokaPipe ALERT: started pipeline for " + sample
        self.email_priority = 3
        self.email_message = sample + " being processed using workflow " + app
        
        # send email
        self.send_an_email()




if __name__ == '__main__':
    # Create instance of get_list_of_runs
    runs = get_list_of_runs()
    # call function
    runs.loop_through_runs()
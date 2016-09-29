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


class get_list_of_runs():
    '''Loop through the directories in the directory containing the runfolders'''
    
    def __init__(self):
        # directory of run folders - must be same as in upload2Nexus()
        self.runfolders ="/media/data1/share" # workstation
        #self.runfolders = "/home/aled/demultiplex_testing" # aledpc
        #self.runfolders = "/home/mokaguys/Documents/upload_agent_test" # workstation dummy

    def loop_through_runs(self):
        # create a list of all the folders in the runfolders directory
        all_runfolders = os.listdir(self.runfolders)
        
        # for each folder if it is not samplesheets pass the runfolder to the next class
        for folder in all_runfolders:
            if folder != "samplesheets":
                if folder.endswith('.gz'):
                    pass
                else:
                    upload2Nexus().already_uploaded(folder)


class upload2Nexus():
    ''' This class is fed a runfolder which may be ready to be uploaded to DNA Nexus''' 
    
    def __init__(self):
        # directory of run folders - must be same as in get_list_of_runs()
        self.runfolders ="/media/data1/share" # workstation
        #self.runfolders = "/home/mokaguys/Documents/upload_agent_test" # workstation dummy
        #self.runfolders = "/home/aled/demultiplex_testing" # aledpc
        
        # file which denotes demultiplexing is underway/complete 
        self.demultiplexed = "demultiplexlog.txt"
        
        # set empty variables to be defined based on the run  
        self.runfolder = ""
        self.runfolderpath = ""

        #succesful run statement
        self.logfile_success="Processing completed with 0 errors and 0 warnings."
        
        # upload started log file
        self.upload_started_file="DNANexus_upload_started.txt"
        
        # upload agent
        self.upload_agent="/home/mokaguys/Documents/apps/dnanexus-upload-agent-1.5.17-linux/ua"
        
        # fastq folder
        self.fastq_folder="Data/Intensities/BaseCalls"
        self.fastq_folder_path=""
        
        #upload_agent_logfile
        self.upload_agent_logfile="/home/mokaguys/Documents/automate_demultiplexing_logfiles/upload_agent_cronjob_log.txt"
        self.upload_agent_script_logfile=open(self.upload_agent_logfile,'a')

        # string of fastqs
        self.fastq_string=""
        
        #create path to data in nexus eg /runfolder/Data
        self.nexus_path= ""
        
        #email server settings
        self.user = 'AKIAIO3XY2MMSBEQNNXQ'
        self.pw   = '***REMOVED***'
        self.host = 'email-smtp.eu-west-1.amazonaws.com'
        self.port = 587
        self.me   = 'gst-tr.mokaguys@nhs.net'
        self.you  = ('gst-tr.mokaguys@nhs.net',)
        self.smtp_do_tls = True
        
        # email message
        self.email_subject=""
        self.email_message=""
        self.email_priority=3
        
    def already_uploaded(self, runfolder):
        '''check folder hasn't already been uploaded'''

        # capture the runfolder 
        self.runfolder = str(runfolder)
               
        # create full path to runfolder
        self.runfolderpath = self.runfolders + "/" + self.runfolder
       
        self.upload_agent_script_logfile.write("\n----------------------"+str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))+"-----------------\nAssessing......... " + self.runfolderpath +"\n")
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
        if os.path.isfile(self.runfolders+"/"+self.runfolder+"/"+self.demultiplexed):
            #open log file
            logfile=open(self.runfolders+"/"+self.runfolder+"/"+self.demultiplexed,'r')
            
            #find the last line of the demultiplexing log file
            lastline=""
            for i in logfile:
                lastline=i
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
        self.fastq_folder_path=self.runfolderpath+"/"+self.fastq_folder
        
        # create a list of all files within the fastq folder
        all_fastqs = os.listdir(self.fastq_folder_path)
        
            
        # find all fastqs
        for fastq in all_fastqs:
            if fastq.endswith('fastq.gz'):
                #exclude undertermined samples 
                if fastq.startswith('Undetermined'):
                    pass
                else:
                    #build the list of fastqs with full file paths
                    self.fastq_string=self.fastq_string+" "+self.fastq_folder_path+"/"+fastq
                    
        #write to logfile
        self.upload_agent_script_logfile.write("list of fastqs found\n")
        
        # send list to module to trigger upload
        self.upload()       
        
    def upload(self):
        '''takes a list of all the fastqs (with full paths) and calls the upload agent.'''
		#self.nexus path
        self.nexus_path=self.runfolder+"/Data"

		# build the nexus upload command                        
        nexus_upload_command = self.upload_agent + " --auth-token kMEShRwrLbRjiqwpol4um1Wi7BpXIHUO --project NGS_runs --folder /"+ self.nexus_path +" --do-not-compress --progress --upload-threads 10 "+ self.fastq_string
        
        #write to logfile
        self.upload_agent_script_logfile.write("Nexus command = \n"+nexus_upload_command+"\n")
        
        #create file to show demultiplexing has started
        upload_started=open(self.runfolderpath+"/"+self.upload_started_file,'w')
        
        # run the command, redirecting stderror to stdout
        proc = subprocess.Popen([nexus_upload_command], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
         
        # capture the streams (err is redirected to out above)
        (out, err) = proc.communicate()
        
        #write to log
        upload_started.write("\n----------------------"+str('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))+"-----------------\n" + out)
        upload_started.close()
        
        

        self.email_subject="Upload of "+self.runfolder+" to DNA Nexus initiated"
        self.email_priority=3
        self.email_message=self.runfolder+" \tuploading to DNA Nexus\nPlease see log file at: "+self.runfolderpath+"/"+self.upload_started_file

        self.send_an_email()


    def send_an_email(self):
        #body = self.runfolder
        self.upload_agent_script_logfile.write("Sending email to...... "+str(self.you))
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
        self.upload_agent_script_logfile.write("Email sent")
        self.upload_agent_script_logfile.close()


if __name__ == '__main__':
    # Create instance of get_list_of_runs
    runs = get_list_of_runs()
    # call function
    runs.loop_through_runs()

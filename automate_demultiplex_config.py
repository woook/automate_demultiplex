"""
Automate demultiplex configuration.

The variables defined in this module are required by the "demultiplex.py" and
"DNANexus_upload_agent.py" scripts.
"""

import os

# Set debug mode
debug = False

# =====location of input/output files=====
# root of folder that contains the apps, automate_demultiplexing_logfiles and development_area scripts
# (2 levels up from this file)
document_root = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-2])

# path to run folders
runfolders = "/media/data3/share"

# samplesheet folder
samplesheets = runfolders + "/samplesheets/"

# path to fastq files
fastq_folder = "/Data/Intensities/BaseCalls"

# path to bcl2fastq
bcl2fastq = "/usr/local/bcl2fastq2-v2.20.0.422/bin/bcl2fastq"

# files for checking NGS runfolders before demultiplexing
file_complete_run = "RTAComplete.txt"
file_demultiplexing = "demultiplexlog.txt"

# directories to be ignored when looping through runfolders
ignore_directories = ["samplesheets", "GlacierTest"]

# runfolders used for debugging/testing
upload_test_folders = ["999999_NB551068_WES_test", "999999_NB551068_custom_panel_test", "999999_M02353_ONC_test"]
demultiplex_test_folder = ["999999_M02353_0288_demultiplex_test"]

# path to log file which records the output of the upload agent
upload_agent_logfile = "{document_root}/automate_demultiplexing_logfiles/upload_agent_script_logfiles/".format(document_root=document_root)

# name of log file which records the output of the upload agent
upload_started_file = "DNANexus_upload_started.txt"

# runfolder backup files
runfolder_upload_cmds = "add_runfolder_to_nexus_cmds.txt"

# Path to DNA Nexus run command log file
DNA_Nexus_workflow_logfolder = "{document_root}/automate_demultiplexing_logfiles/dx_run_commands/".format(document_root=document_root)

# log folder containing project creation logs
DNA_Nexus_project_creation_logfolder = "{document_root}/automate_demultiplexing_logfiles/nexus_project_creation_scripts/create_nexus_project_".format(document_root=document_root)

# folder containing demultiplex logs
demultiplex_logfiles = "{document_root}/automate_demultiplexing_logfiles/Demultiplexing_log_files/".format(document_root=document_root)

# path to upload agent
upload_agent_path = "{document_root}/apps/dnanexus-upload-agent-1.5.17-linux/ua".format(document_root=document_root)
#upload_agent_path = "/usr/local/src/mokaguys/apps/dnanexus-upload-agent-1.5.17-linux/ua"
upload_agent_test_command = " --version"
ua_error = "Error Message: 'Could not resolve: api.dnanexus.com"

# path to backup_runfolder script
backup_runfolder_script = "/usr/local/src/mokaguys/apps/workstation_housekeeping/backup_runfolder.py"

# backup runfolder folder
backup_runfolder_logfile = "/usr/local/src/mokaguys/automate_demultiplexing_logfiles/backup_runfolder_logfiles"
backup_runfolder_success = "backup_runfolder INFO - END"

# command to test dx toolkit
# dx_sdk_test = "source /etc/profile.d/dnanexus.environment.sh;dx --version"
dx_sdk_test = "source ~/dx-toolkit/environment;dx --version"
# expected result from testing
dx_sdk_test_expected_stdout = "dx v0.2"

upload_agent_expected_stdout = "Upload Agent Version:"

# =====Moka settings=====
# Moka IDs for generating SQLs to update the Mokadatabase
# Current Mokapipe ID
mokapipe_pipeline_ID = "3559"
# Current MokaWES ID
mokawes_pipeline_ID = "3053"

# -- Moka WES test status--
# Test Status = NextSEQ sequencing
mokastat_nextsq_ID = "1202218804"
# Test Status = Data Processing
mokastatus_dataproc_ID = "1202218805"

# =====DNA Nexus settings=====
# project to upload run folder into
NexusProjectPrefix = "002_"

# success statement when creating project
project_success = "Created new project called \"%s\""

# The project containing the app and data
app_project = "001_ToolsReferenceData:/"
# path to the workflow in the app project
mokapipe_path = "Workflows/GATK3.5_v2.11"
# path to the WES workflow in the app project
mokawes_path = "Workflows/MokaWES_v1.5"
# path to the oncology workflow in the app project
mokaonc_path = "Workflows/Mokaonc_v1.4"
# path to mokaamp
mokaamp_path = "Workflows/MokaAMP_v1.2"
# path to paddy app
peddy_path = "Apps/peddy_v1.3"
# path to multiqc app
multiqc_path = "Apps/multiqc_v1.11"
# path to senteion upload app
sapientia_app_path = "Apps/sapientia_upload_v1.0"
# path to iva upload app
iva_app_path = "app-ingenuity_variant_transfer/1.0.6"
# path to app which uploads multiqc report
upload_multiqc_path = "Apps/upload_multiqc_v1.1"
# smartsheet app
smartsheet_path = "Apps/smartsheet_mokapipe_complete_v1.1"
# RPKM path
RPKM_path = "Apps/RPKM_using_conifer_v1.5"
# bedfile folder
bedfile_folder = "Data/BED/"
# DNA Nexus organisation to create the project within
prod_organisation = "org-viapath_prod"
dev_organisation = "org-viapath_dev"

# project tags to denote live cases
live_tag = "live"

# =====istages=====
# Mokapipe workflow inputs
mokapipe_fastqc1 = " -istage-Bz3YpP80jy1Y1pZKbZ35Bp0x.reads="  # FastQC Read 1
mokapipe_fastqc2 = " -istage-Bz3YpP80jy1x7G5QfG3442gX.reads="  # FastQC Read 2
mokapipe_bwa_rg_sample = " -istage-Byz9BJ80jy1k2VB9xVXBp0Fg.read_group_sample=" # bwa rg samplename
mokapipe_sambamba_input = " -istage-F35zBKQ0jy1XpfzYPZY4bgX6.sambamba_bed="  # Sambamba Bed file
mokapipe_mokapicard_vendorbed_input = " -istage-F9GK4QQ0jy1qj14PPZxxq3VG.vendor_exome_bedfile="  # HSMetrics Bed file
mokapipe_iva_email_input = " -istage-Byz9Bj80jy1k2VB9xVXBp0Fp.email="  # ingenuity email address
mokapipe_variant_annotator_stage = "stage-F2gPqFQ025p601qgGq0QVvX2"
mokapipe_gatk_human_exome_stage = "stage-F28y4qQ0jy1fkqfy5v2b8byx"
mokapipe_vcf_output_name = "vcf"
mokapipe_bam_output_name = "bam"


# MokaWES workflow_inputs
wes_fastqc1 = " -istage-Bz3YpP80jy1Y1pZKbZ35Bp0x.reads="  # FastQC Read 1
wes_fastqc2 = " -istage-Bz3YpP80jy1x7G5QfG3442gX.reads="  # FastQC Read 2
wes_picard_bedfile = " -istage-F9GGBQj0jy1yBbpZPvK5GvPJ.vendor_exome_bedfile=" # bedfile for hs metrics
senteion_stage_id = "stage-FQ8JPpj076Gybkq459GfqfZb"
wes_sambamba_bedfile = " -istage-F35zBKQ0jy1XpfzYPZY4bgX6.sambamba_bed="
wes_sention_samplename = " -i%s.sample=" % senteion_stage_id # sample name for sention app - prevents sample being incorrectly parsed from fastq filename
wes_sention_targets_bed = " -i%s.targets_bed=" % senteion_stage_id # BED file used to restrict Senteion variant calling
wes_ingenuity_email = " -istage-Byz9Bj80jy1k2VB9xVXBp0Fp.email="

# MokaOnc amplivar fastq input
mokaonc_fq_input = " -istage-F7kPz6Q0vpxb0YpjBgQx5f8v.fastqs="
mokaonc_ingenuity = " -istage-F5k1Qyj0jy1VKJb2KYqq7fxG.email="  # ingenuity app input for amplivar workflow

# MokaAMP
mokaamp_fastq_R1_stage = " -istage-FPzGj780jy1g3p1F4F8z4J7V.reads_fastqgz="
mokaamp_fastq_R2_stage = " -istage-FPzGj780jy1g3p1F4F8z4J7V.reads2_fastqgz="
mokaamp_mokapicard_bed_stage = " -istage-FPzGjV80jy1x97jg607Fg22b.vendor_exome_bedfile="
mokaamp_mokapicard_capturetype_stage = " -istage-FPzGjV80jy1x97jg607Fg22b.Capture_panel="
mokaamp_bamclipper_BEDPE_stage = " -istage-FPzGjJQ0jy1fF6505zFP6zz9.primers="
mokaamp_chanjo_cov_level_stage = " -istage-FPzGjfQ0jy1y01vG60K22qG1.coverage_level="
mokaamp_sambamba_bed_stage = " -istage-FPzGjfQ0jy1y01vG60K22qG1.sambamba_bed="
mokaamp_vardict_bed_stage = " -istage-FPzGjgj0jy1Q2JJF2zYx5J5k.bedfile="
mokaamp_varscan_bed_stage = " -istage-FPzGjp80jy1V3Jvb5z6xfpfZ.bed_file="
mokaamp_varscan_strandfilter_stage = " -istage-FPzGjp80jy1V3Jvb5z6xfpfZ.strand_filter="
mokaamp_lofreq_bed_stage = " -istage-FPzGjgQ0jy1fBy972zq9f1PY.bedfile="

mokaamp_strandfilter = "True"
mokaamp_coverage_level = "1000"
mokaamp_capture_type = "Amplicon"
mokaamp_email_message = "If both MokaAMP and MokaOnc (amplivar) have been run, please record the version of MokaOnc used."

# Peddy
peddy_project_input = " -iproject_for_peddy="

# MultiQC and upload_multiqc inputs, outputs and variables
multiqc_project_input = " -iproject_for_multiqc="
multiqc_coverage_level_input = " -icoverage_level="
multiqc_html_output = "multiqc_report"
upload_multiqc_input = " -imultiqc_html="
wes_multiqc_coverage_level = "20"  # HSMetrics coverage level to be reported for wes
custom_panel_multiqc_coverage_level = "30"  # HSMetrics coverage level to be reported for custom panel
mokaamp_multiqc_coverage_level = "100"  # HSMetrics coverage level to be reported for mokaamp

# Smartsheet
smartsheet_mokapipe_complete = " -iNGS_run="

# RPKM inputs
rpkm_bedfile_input = " -ibedfile="
rpkm_project_input = " -iproject_name="
rpkm_bamfiles_to_download_input = " -ibamfile_pannumbers="

# emails addresses for Ingenuity
oncology_email = 'gst-tr.oncology.interpret@nhs.net'  # general oncology email
interpretation_request_email = "gst-tr.interpretation.request@nhs.net"  # email for Interpretation_requests
wes_email_address = "gst-tr.wesviapath@nhs.net" # WES email

# DNA Nexus authentication token
nexus_api_key_file = "{document_root}/.dnanexus_auth_token".format(document_root=document_root)
with open(nexus_api_key_file, 'r') as nexus_api:
    Nexus_API_Key = nexus_api.readline().rstrip()

# list of DNA Nexus users with view access to project
view_users = ["org-viapath_prod", "InterpretationRequest"]
# list of DNA Nexus users with admin access of project
admin_users = ["mokaguys"]

# =====Decision support script
# takes an analysis id and builds inputs for the decision support upload.
decision_support_tool_input_script = "decision_support_tool_inputs.py"
mokawes_senteion_bam_output_name = "mappings_realigned_bam"
mokawes_senteion_bai_output_name = "mappings_realigned_bai"
mokawes_senteion_vcf_output_name = "variants_vcf"
sapientia_vcf_inputname = " -ivcf="
sapientia_bam_inputname = " -ibam="
iva_vcf_inputname = " -ivcfs="
iva_bam_inputname = " -ibam_files="
iva_bai_inputname = " -ibai_files="
iva_email_input_name = " -iemail="
iva_reference_inputname = " -ireference_genome_name="
iva_reference_default = "GRCh37"


# =====Dict linking panel numbers for +/-10 and CNVs=====
panel_list = ["Pan493", "Pan1063", "Pan1190", "Pan2684", "Pan1449", "Pan2022", "Pan1965", "Pan1158", "Pan1159", "Pan1646", "Pan3320"]#, "Pan3321"]
default_panel_properties = {
                    "UMI": False,
                    "UMI_bcl2fastq": None, # eg Y145,I8,Y9I8,Y145
                    "RPKM_bedfile_pan_number": None,
                    "RPKM_also_analyse": None, # This is a comma seperated list containing additional pan numbers that decribe which BAM files should be downloaded
                    "onePGT": False,
                    "mokawes": False,
                    "joint_variant_calling": False,
                    "mokaamp": False,
                    "capture_type": "Hybridisation", # "Amplicon" or "Hybridisation"
                    "mokaonc": False,
                    "mokapipe": False,
                    "mokaamp_varscan_strandfilter": True,
                    "iva_upload": False,
                    "sapientia_upload": False,
                    "oncology": False,
                    "clinical_coverage_depth": None, # only found in mokamp command
                    "multiqc_coverage_level": 30,
                    "hsmetrics_bedfile": None, # only when using bed file with a different pannumber
                    "mokawes_variant_calling_bedfile": None, # only when using bed file with a different pannumber
                    "sambamba_bedfile": None, # only when using bed file with a different pannumber
                    "ingenuity_email": interpretation_request_email,
                    "sapientia_project": None,
                    "peddy": False
                }

# override default panel settings
panel_settings = {"Pan493": {
                    "mokawes": True,
                    #"iva_upload": True,
                    "multiqc_coverage_level": 20,
                    "hsmetrics_bedfile": "agilent_sureselect_human_all_exon_v5_b37_targets.bed", # only when using bed file with a different pannumber
                    "mokawes_variant_calling_bedfile": "agilent_sureselect_human_all_exon_v5_b37_padded.bed", # only when using bed file with a different pannumber
                    "ingenuity_email":wes_email_address,
                    "peddy": True
                    },
                "Pan2835": {# TWIST WES at GSTT
                    "mokawes": True,
                    #"iva_upload": True,
                    "multiqc_coverage_level": 20,
                    # uncomment after mokabed PR
                    #"hsmetrics_bedfile": "Twist_Exome_RefSeq_CCDS_v1.2_targets.bed", # only when using bed file with a different pannumber
                    #"mokawes_variant_calling_bedfile": "Twist_Exome_RefSeq_CCDS_v1.2_padded.bed", # only when using bed file with a different pannumber
                    "ingenuity_email":wes_email_address,
                    "peddy": True
                    },
                # "Pan3321": {# TWIST singleton WES at STG
                #     "mokawes": True,
                #     "sapientia_upload": True,
                #     #"sapientia_project": "1099",#live service
                #     "sapientia_project": "261", # testing
                #     "multiqc_coverage_level": 20,
                #     # uncomment after mokabed PR
                #     #"hsmetrics_bedfile": "Twist_Exome_RefSeq_CCDS_v1.2_targets.bed", # only when using bed file with a different pannumber
                #     #"mokawes_variant_calling_bedfile": "Twist_Exome_RefSeq_CCDS_v1.2_padded.bed", # only when using bed file with a different pannumber
                #     "peddy": True
                #     },
                # "Pan1620": { # Focused Exome. Are we uploading to Ingenuity? Note: NO vendorexome bedfile
                #     "mokawes": True,
                #     "ingenuity_email":wes_email_address,
                #     #"iva_upload": True
                #     },
                "Pan1190": { # EGFR SWIFT Panel
                    "mokaamp": True,
                    "oncology": True,
                    "mokaonc": True,
                    "capture_type": "Amplicon",
                    "ingenuity_email":oncology_email,
                    "clinical_coverage_depth":1000,
                    "multiqc_coverage_level": 100,
                    "iva_upload": True
                    },
                "Pan2684": { # 57G panel
                    "RPKM_bedfile_pan_number": None,
                    "mokaamp": True,
                    "oncology": True,
                    "capture_type": "Amplicon",
                    "iva_upload": True,
                    "clinical_coverage_depth":600, # only found in mokamp command
                    "multiqc_coverage_level":100,
                    "ingenuity_email":oncology_email
                },
                "Pan1449": { # germline BRCA
                    "mokapipe": True,
                    "multiqc_coverage_level": 30,
                    "RPKM_bedfile_pan_number": "Pan1450",
                    "RPKM_also_analyse": ["Pan3320"],
                    "iva_upload": True
                    },
                "Pan3320": { # STG germline BRCA
                    "mokapipe": True,
                    "multiqc_coverage_level": 30,
                    "RPKM_bedfile_pan_number": "Pan1450",
                    "RPKM_also_analyse": ["Pan1449"],
                    "sapientia_upload": True,
                    #"sapientia_project": "1099",#live service
                    "sapientia_project": "261", # testing
                    "hsmetrics_bedfile": "Pan1449", # only when using bed file with a different pannumber
                    "sambamba_bedfile": "Pan1449" # only when using bed file with a different pannumber
                    },
                "Pan1063": { # IMDv2
                    "mokapipe": True,
                    "multiqc_coverage_level": 30,
                    "RPKM_bedfile_pan_number": "Pan1064",
                    "iva_upload": True
                    },
                "Pan2022": { # CMCMD
                    "mokapipe": True,
                    "multiqc_coverage_level": 30,
                    "RPKM_bedfile_pan_number": "Pan1974",
                    "iva_upload": True
                    },
                "Pan1965": { # NGSEQ1
                    "mokapipe": True,
                    "multiqc_coverage_level": 30,
                    "RPKM_bedfile_pan_number": "Pan2000",
                    "iva_upload": True
                    },
                "Pan1158": { # NGSEQ2
                    "mokapipe": True,
                    "multiqc_coverage_level": 30,
                    "RPKM_bedfile_pan_number": "Pan2023",
                    "iva_upload": True
                    },
                "Pan1159": { # NGSEQ3
                    "mokapipe": True,
                    "multiqc_coverage_level": 30,
                    "RPKM_bedfile_pan_number": "Pan1973",
                    "iva_upload": True
                    },
                "Pan1646": { # ICTHYOSIS - use same settings as WES and Pan1646 for coverage
                    "mokawes": True,
                    #"iva_upload": True,
                    "multiqc_coverage_level": 20,
                    "hsmetrics_bedfile": "agilent_sureselect_human_all_exon_v5_b37_targets.bed", # only when using bed file with a different pannumber
                    "mokawes_variant_calling_bedfile": "agilent_sureselect_human_all_exon_v5_b37_padded.bed", # only when using bed file with a different pannumber
                    "ingenuity_email":wes_email_address,
                    "peddy": True
                    }
                }

# =====smartsheet API=====
# smartsheet sheet ID
smartsheet_sheetid = 2798264106936196

# API key
smartsheet_api_key_file = "{document_root}/.smartsheet_auth_token".format(document_root=document_root)
with open(smartsheet_api_key_file, 'r') as ss_api:
    smartsheet_api_key = ss_api.readline().rstrip()

# columnIds
ss_title = 6197963270711172
ss_description = 3946163457025924
ss_samples = 957524288530308
ss_status = 8449763084396420
ss_priority = 4790588387157892
ss_assigned = 2538788573472644
ss_received = 6723667267741572
ss_completed = 4471867454056324
ss_duration = 6519775204534148
ss_metTAT = 4267975390848900

# ================ Requests info
smartsheet_request_headers = {"Authorization": "Bearer " + smartsheet_api_key, "Content-Type": "application/json"}
smartsheet_request_url = 'https://api.smartsheet.com/2.0/sheets/' + str(smartsheet_sheetid)

# =================turnaround time
# if a task takes more than this amount of time it is out of TAT
allowed_time_for_tasks = 4

# =================== Email server settings
mokaguys_email = 'gst-tr.mokaguys@nhs.net'
username_file_path = '{document_root}/.amazon_email_username'.format(document_root=document_root)
with open(username_file_path, 'r') as username_file:
    user = username_file.readline().rstrip()
pw_file = '{document_root}/.amazon_email_pw'.format(document_root=document_root)
with open(pw_file, 'r') as email_password_file:
    pw = email_password_file.readline().rstrip()
host = 'email-smtp.eu-west-1.amazonaws.com'
port = 587
me = 'moka.alerts@gstt.nhs.uk'
you = mokaguys_email
oncology_you = oncology_email
smtp_do_tls = True

# ================ Integrity check
# the filename which holds the checksum results
md5checksum_name = "md5checksum.txt"
# checksum complete statement
checksum_complete_flag = "Checksum result reported"
# statement to write when checksums match
checksum_match = "Checksums match"

# ================ demultiplexing
demultiplex_success_string = "Processing completed with 0 errors and 0 warnings."
# list of sequencers which require md5 checksums from integrity check to be assessed
sequencers_with_integrity_check = ["NB551068", "NB552085"]



#! /usr/bin/env python
def process(transaction):
    import os
    inc_file        = transaction.getIncoming() # incoming file
    inc_directory   = transaction.getIncoming().getAbsolutePath() # incoming filepath
    filename        = inc_file.getName()
    filetype        = filename.split('.')[1]
    filename_without_type = filename.split('.')[0]

    space = '502ICA_PROJECTS'
    project = 'CP_ANALYSES'
    parts = filename_without_type.split("_")

    if filetype.lower() == 'raw' and len(parts >=5):  # split the filename with underscores
        
        # log content
        transaction.getLogger().info('Adding valid raw file')
        transaction.getLogger().info('Directory: '+ inc_directory+ 'Filename:  '+ filename)
        for part in parts:
            transaction.getLogger().info(part)

        # read from the filename and partition
        experiment = parts[0]
        batch_no = parts[1]
        sample_type = parts[2]
        injection_no = parts[3]
        samplename = parts[4:]

        if sample_type == 'A':
            sample_type = "ANALYTE"
        elif sample_type == 'B':
            sample_type = "BLANK"
        elif sample_type == 'IS':
            sample_type = "STANDARD"
        elif sample_type == 'S':
            sample_type = "SOLVENT"
        elif sample_type == 'SM':
            sample_type = "STAND_MATERIAL"
        else: sample_type = None
                        
        # get experiment
        sampleid = "/%(space)s/%(project)s/%(experiment)s/%(samplename)s" % vars()
        transaction.getLogger().info('The sample_id is %s' % (sampleid))
        sample = transaction.getSample(sampleid)      
    
        # create a sample if no sample exists and give it all properties
        if sample == None:
            transaction.getLogger().info('Sample with id %s not found. Creating...' % (sampleid))
            sample = transaction.createNewSample(sampleid, 'LC_MS_CP')
            sample.setPropertyValue("CP_BATCH_NUMBER", batch_no)
            sample.setPropertyValue("NUMBER_OF_INJECTION", injection_no)
            sample.setPropertyValue("$NAME", samplename)
            if sample_type != None:
                sample.setPropertyValue("CHEMICALS.TYPE", sample_type)

        # create new dataset and attach it to the sample
        dataSet = transaction.createNewDataSet()
        dataSet.setPropertyValue("$NAME", filename_without_type);
        dataSet.setDataSetType("MS_DATA")
        dataSet.setSample(sample)
        
        # move the file to the dataset
        transaction.moveFile(inc_directory, dataSet) # move the file
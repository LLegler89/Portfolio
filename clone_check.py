# This function requires 2 inputs with 2 optional arguments
# Required = Path to plasmid sequences (fasta or .seq directory)
# optional = 3' and 5' Flanking sequences on the plasmid to check for insertion or deletion of bp at the cloning site during ligation.

def clone_check(seq_filepath, guide_filepath, output_directory, _3_prime="", _5_prime=""):

  !pip install biopython
  import Bio
  from Bio import SeqIO
  import os
  import openpyxl

  ### Define functions

  def process_seq_files(directory):

    directory_path = seq_filepath

    sequences = open(output_directory + "/output.fasta", "w")

    for filename in os.listdir(directory_path):
        # Check if the file ends with .seq
        if filename.endswith(".seq"):
           # Get the full path of the file
          file_path = os.path.join(directory_path, filename)
           # Read the contents of the file
          with open(file_path, "r") as f:
              sequence = f.read()

            # Print the sequence in FASTA format
          print(f">{filename}", file=sequences)
          print(sequence, file=sequences)
          print(f">{filename}")
          print(sequence)
    sequences.close()
  
    return output_directory + "/output.fasta"




  def fasta_to_list(fasta_file):

    # Initialize an empty list to store the data.
    data = []

    with open(fasta_file, 'r') as f:
      lines = f.readlines()

    # Iterate over the lines.
    current_sample = None
    current_sequence = []
    for line in lines:
      # Check if the line starts with '>'.
      if line.startswith('>'):
        # If it does, it's a new sample.
        # Store the previous sample's data (if any).
        if current_sample is not None:
          data.append([current_sample, ''.join(current_sequence)])
        # Start a new sample.
        current_sample = line.strip()[1:]
        current_sequence = []
      else:
        # Otherwise, it's part of a sequence.
        current_sequence.append(line.strip())

    # Store the last sample's data.
    if current_sample is not None:
      data.append([current_sample, ''.join(current_sequence)])

    # Return the data.
    return data




  def excel_to_list(excel_file):


    # Open the excel file.
    workbook = openpyxl.load_workbook(excel_file)

    # Get the active sheet.
    sheet = workbook.active

    # Initialize an empty list to store the data.
    data = []

    # Iterate over the rows in the sheet.
    for row in sheet.iter_rows():
      # Initialize an empty list to store the current row's data.
      row_data = []
 
      # Iterate over the cells in the current row.
      for cell in row:
        # Append the cell's value to the row_data list.
        row_data.append(cell.value)

      # Append the row_data list to the data list.
      data.append(row_data)

    # Return the data.
    return data


  def is_directory(path):
    return os.path.isdir(path)

  def is_fasta_file(path):
    _, extension = os.path.splitext(path)
    return extension.lower() == '.fasta'

  def determine_argument_type(path):
    if is_directory(path):
      return "directory"
    elif is_fasta_file(path):
      return "fasta_file"
    else:
      return None




  # Determine file type and produce sequence lists

  if determine_argument_type(seq_filepath) == 'directory':
    data = process_seq_files(seq_filepath)
    data = fasta_to_list(data)
    data_type = 'directory'
  elif determine_argument_type(seq_filepath) == 'fasta_file':
    data= fasta_to_list(seq_filepath)
    data_type = 'fasta_file'
  else:
    return "Error in processing. Input is neither a directory or fasta file"
    
  # Read and sort the data for final processing
  
  data = sorted(data, key=lambda x: x[0])
  guide_ref = excel_to_list(guide_filepath)
  results = []

  

  for i in range(len(data)):
    if (_3_prime + guide_ref[i][1] + _5_prime) in data[i][1]:
      results.append(f"Congratulations! {guide_ref[i][0]} was perfectly cloned into {data[i][0]}")
    elif guide_ref[i][1] in data[i][1]:
      results.append(f"Unfortunately, {guide_ref[i][0]} guide was successfully cloned into {data[i][0]}, but off-target base pairs were added or removed")
    else:
      results.append(f":( Sorry, {guide_ref[i][0]} not found in {data[i][0]}. Keep trying, you've got this!")

  print(results)

  #Generate results file

  f = open(output_directory + "/clone_check_results.txt", 'w')
  for i in results:
    print(i, file = f)
  f.close()

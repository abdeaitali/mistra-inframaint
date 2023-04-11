function [H_table_MB5,H_table_MB6] = read_input_data()
%READ_INPUT_DATA Reads simulation results
%   Based on simulation results, this function reads resulting tables

% read table with mechanical simulation results
filename = "./Wear/mistra_results.xlsx";
sheet = "H_30t";
xlRange_MB5 = "B3:M6";
xlRange_MB6 = "B8:M9";
H_table_MB5 = xlsread(filename,sheet,xlRange_MB5);
H_table_MB6 = xlsread(filename,sheet,xlRange_MB6);

end


function [prev,korr,renewal,headers] = read_input_data()
%READ_INPUT_DATA Summary of this function goes here
%   Detailed explanation goes here

% read table with mechanical simulation results
filename = "./data_sc_LCC.xlsx";
xlRange = "B3:X47";
prev = xlsread(filename,"prev",xlRange);
korr = xlsread(filename,"korr",xlRange);
renewal = xlsread(filename,"renewal","B2:B24");

% convert from cummulative to yearly increments
for t=1:45
    row = 45-(t-1);
    if(row>1)
        prev(row,:) = prev(row,:) - prev(row-1,:);
        korr(row,:) = korr(row,:) - korr(row-1,:);
    end
end


% Read headers
[~, headers] = xlsread(filename, "prev", "B1:X1", 'basic');



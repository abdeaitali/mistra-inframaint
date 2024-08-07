function [prev,korr,fail,renewal,MGT,nb_freight_year,nb_pass_year,delay_min,MGT_lifetime,headers, ERS] = read_input_data()
%READ_INPUT_DATA Summary of this function goes here
%   Detailed explanation goes here

% read table with mechanical simulation results
filename = "./data_sc_LCC.xlsx";
xlRange = "B3:H77";
time_horizon_max = 75;
% regression result tables for different switch models
prev = xlsread(filename,"prev",xlRange);
korr = xlsread(filename,"korr",xlRange);
fail = xlsread(filename,"failure",xlRange);
% extra input
renewal = xlsread(filename,"extra","G2:G8");
MGT = xlsread(filename,"extra","B2:B8");
% nb_train_year = xlsread(filename,"extra","C2:C8");
nb_freight_year = xlsread(filename,"extra","D2:D8");
nb_pass_year = xlsread(filename,"extra","E2:E8");
delay_min = xlsread(filename,"extra","F2:F8");
MGT_lifetime = xlsread(filename,"extra","H2:H8");
[~, headers] = xlsread(filename, "extra", "A2:A8", 'basic');% Read headers
% Reimbursement rules
ERS_prev = xlsread(filename,"ERS","B3:I77");
ERS_korr = xlsread(filename,"ERS","B79:I153");
ERS_fail = xlsread(filename,"ERS","B155:I229");
% convert from cummulative to yearly increments
factor = linspace(1,1,75);
for y=1:time_horizon_max
    row = time_horizon_max-y+1;
    if(row>1)
        prev(row,:) = prev(row,:) - prev(row-1,:);
        korr(row,:) = korr(row,:) - korr(row-1,:);
        fail(row,:) = fail(row,:) - fail(row-1,:);
        % Reimbursement rules
        ERS_prev(row,:) = ERS_prev(row,:) - ERS_prev(row-1,:);
        ERS_korr(row,:) = ERS_korr(row,:) - ERS_korr(row-1,:);
        ERS_fail(row,:) = ERS_fail(row,:) - ERS_fail(row-1,:);
    end
    % amplify !!!
    korr(row,:) = factor(row)*korr(row,:);
    prev(row,:) = factor(row)*prev(row,:);
    fail(row,:) = factor(row)*fail(row,:);
    % ERS
    ERS_korr(row,:) = factor(row)*ERS_korr(row,:);
    ERS_prev(row,:) = factor(row)*ERS_prev(row,:);
    ERS_fail(row,:) = factor(row)*ERS_fail(row,:);    
end
ERS = {ERS_prev, ERS_korr, ERS_fail};

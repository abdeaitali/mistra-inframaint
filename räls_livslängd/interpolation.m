function [H_table_interpol] = interpolation(H_table, type, grinding_freq_max, tonnage)
%INTERPOLATION Interpolation of the H-index look-up table
%   Given a specific interpolation method, this function replaces the values 
%   of the first months with an interpolation
  

%%% the indices of the months
Yq = [0,7,8,9,10,11,12];% months
if(strcmp(tonnage,'H_30t')) % if heavy axle load, use other points
    Yq = [0,7,8,9,10]; % months
end
%%% the indices of the track gauges (in mm)
gauge = [1440,1445,1450,1455];

%%% interpolation for one year (12 months)
Xq = [1440,1455];
H_table_interpol = zeros(4,grinding_freq_max);
ext_H_table = [zeros(size(gauge,2),1) H_table];
for g_id=1:size(gauge,2)
    for m=1:12
        H_table_interpol(g_id,m) = ...
            interp2(Yq,gauge, ext_H_table(:,Yq+1), m, gauge(g_id),type);
        if(H_table_interpol(g_id,m)<0)
            H_table_interpol(g_id,m) = 0;
        end
    end
    for m=13:grinding_freq_max
        H_table_interpol(g_id,m) = ...
            interp1(1:12, H_table_interpol(g_id,1:12), m, type, 'extrap'); 
        if(H_table_interpol(g_id,m)<0)
            H_table_interpol(g_id,m) = 0;
        end
    end
end




    
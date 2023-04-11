function [H_table_interpol] = interpolation(H_table)
%INTERPOLATION Summary of this function goes here
%   Detailed explanation goes here

% gauge intervals (in mm)
gauge = [1440,1445,1450,1455];

% interpolations of H table
H_table_interpol = zeros(size(gauge,2),12); % after 6 or 12 months
Xq = gauge;
Yq = [0,1,10,11,12]; % months
ext_H_table = [zeros(size(gauge,2),1) H_table]; 
for g_id=1:size(gauge,2)
    for m=1:12
        H_table_interpol(g_id,m) = interp2(Xq, Yq, ext_H_table(:,Yq+1)', gauge(g_id), m,'linear');
    end
end
end


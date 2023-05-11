function [H_table_interpol] = interpolation(H_table, type)
%INTERPOLATION Summary of this function goes here
%   Detailed explanation goes here
% gauge intervals (in mm)
gauge = [1440,1445,1450,1455];

% interpolations of H table
H_table_interpol = zeros(size(gauge,2),12); % after 6 or 12 months
Yq = [0,6,7,8,9,10,11,12]; % months
%Yq = [0,6,12]; % for cubic

if(size(H_table,1)==2) % MB6
   
    % interpolations of H table
    ext_H_table = [zeros(size(gauge,2),1) H_table_interpol];
    ext_H_table(3:4,2:end) = H_table;
    ext_H_table(1,2:end) = H_table(1,1);
    Xq = [1,3,4];
    for g_id=1:size(gauge,2)
        for m=1:12
            H_table_interpol(g_id,m) = interp2(gauge(Xq), Yq, ext_H_table(Xq,Yq+1)', gauge(g_id), m,type);
        end
    end
    
else % MB5
 
    Xq = gauge;
    ext_H_table = [zeros(size(gauge,2),1) H_table];
    for g_id=1:size(gauge,2)
        for m=1:12
            H_table_interpol(g_id,m) = interp2(Xq, Yq, ext_H_table(:,Yq+1)', gauge(g_id), m,type);
        end
    end
end

end




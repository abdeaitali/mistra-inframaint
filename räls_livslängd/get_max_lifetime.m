function [max_lifetime] = get_max_lifetime(risk)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% set parameter for threeshold (in months) for 1455mm
param_threshold_1455 = 4;

% find the max lifetime for the others
max_lifetime = zeros(size(risk,1),1);
max_lifetime(end) = param_threshold_1455;
for g=1:size(risk,1)-1
    for m=param_threshold_1455:12
        if(risk(g,m)<=risk(end,param_threshold_1455))
            max_lifetime(g) = m;
        else
            break;
        end
    end
end

% in case of MB6, append gauges with max lifetime = 12 months
if(size(risk,1)==2)
    max_lifetime = [12;12;max_lifetime];
end

end


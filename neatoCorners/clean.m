
function xy = clean(pos)
xy = [];
%Treure punts (0,0)
for i=1:1:length(pos)
    if pos(i,1) ~= 0 && pos(i,2) ~= 0
       xy = [xy; pos(i,:)];       
    end
end
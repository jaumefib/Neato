
function xy = cantonades(points)
xy = [];
w = 6; %30;
max_dist = 10000000; %5000;
for i=1:1:length(points)-w
    dist = sqrt((points(i+w,1)-points(i,1))^2 + (points(i+w,2)-points(i,2))^2);
    if dist < max_dist
        ux = points(i+w,1) - points(i+w/2,1);
        uy = points(i+w,2) - points(i+w/2,2);
        vx = points(i+w/2,1) - points(i,1);
        vy = points(i+w/2,2) - points(i,2);
        pas2 = (ux*vx) + (uy*vy);
        pas3 = sqrt(ux^2 + uy^2) * sqrt(vx^2 + vy^2);
        pas1 = pas2/pas3;
        beta = acos(pas1)*(180/pi);
        if (beta > 80 && beta < 100) || (beta > 260 && beta < 280)
            xy = [xy; points(i+3,:)];
        end
    end
end
end
clc 
clear all 
close all 

hFig = figure;
x      = 0;   % Screen position
y      = 0;   % Screen position
width  = 1100; % Width of figure
height = 720;
set(hFig, 'Position', [x y width height])

subplot (2,2,1)
fname1=fopen('../Host_15/HD_10.txt', 'r');
val=textscan(fname1,'%d %f', 'HeaderLines',1);
% celldisp(val)
fclose(fname1);
Packet_num1=val{1};
latency1=val{2};
delay1=val{2}/1000;
plot(Packet_num1,delay1,':b','LineWidth', 1.5)
xlabel(['No. of packets', newline,'\bf (a)'],'FontSize', 15,'FontName','Times New Roman')
ylabel ( 'Packet latency (ms)','FontSize' , 15,'FontName','Times New Roman')


a = get(gca,'XLabel');
b = get(gca,'YLabel');
set(gca,'YLabel',b,'FontName','Times','fontsize',12)
set(gca,'XLabel',a,'FontName','Times','fontsize',12)

xticks([0,2, 4,6 8, 10]);
yticks('auto');
xlim([-0.1, 10.1])
ylim([0 15])

subplot (2,2,2)
fname2=fopen('../Host_15/HD_100.txt', 'r');
val=textscan(fname2,'%d %f', 'HeaderLines',1);
fclose(fname2);
Packet_num2=val{1};
latency2=val{2};
delay2=val{2}/1000;
plot(Packet_num2,delay2,'-.m','LineWidth', 1.5)
xlabel(['No. of packets', newline,'\bf (b)'],'FontSize', 15,'FontName','Times New Roman')
ylabel ( 'Packet latency (ms)','FontSize' , 15,'FontName','Times New Roman','HorizontalAlignment', 'center')



a = get(gca,'XLabel');
b = get(gca,'YLabel');
set(gca,'YLabel',b,'FontName','Times','fontsize',12)
set(gca,'XLabel',a,'FontName','Times','fontsize',12)

xticks([0,20, 40,60 80, 100]);
yticks('auto');
xlim([-1, 101])
ylim([0 15])

h=subplot (2,2,3);
fname3=fopen('../Host_15/HD_1000.txt', 'r');
val=textscan(fname3,'%d %f', 'HeaderLines',1);
fclose(fname3);
Packet_num3=val{1};
latency3=val{2};
delay3=val{2}/1000;
plot(Packet_num3,delay3,'-r','LineWidth', 1)
xlabel(['No. of packets', newline,'\bf (c)'],'FontSize', 15,'FontName','Times New Roman')
ylabel ( 'Packet latency (ms)','FontSize' , 15,'FontName','Times New Roman','HorizontalAlignment', 'center')

a = get(gca,'XLabel');
b = get(gca,'YLabel');
set(gca,'YLabel',b,'FontName','Times','fontsize',12)
set(gca,'XLabel',a,'FontName','Times','fontsize',12)

xticks([0,200, 400,600 800, 1000]);
xtickformat('%,4.4g')
yticks('auto');
xlim([-10, 1010])
ylim([0, 15])

% Align the third subplot to the middle of the row
pos = get(h, 'position');
pos(1) = 0.35; % Adjust the horizontal position to align to the middle
set(h, 'position', pos);


set(hFig,'PaperSize',[10 7.5]);
print(hFig,'NoML_Latency_Plot_H15','-dpdf') % then print it
% print(hFig,'Direct_Latency_Plot','-dtiff') % then print it

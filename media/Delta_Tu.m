% Die zwei letzten Temperaturwerte werden vom Channel motor_1 
% gelesen. Die Änderung wird berechnet und in das Feld 1 channel motor_1_calc geschrieben

% Channel ID to read data from
readChannelID = 381619;
% Tu Field ID
TuFieldID = 1;
% Channel Read API Key; siehe rechte Spalte 
readAPIKey = 'TZU1G2WP033AGCEJ';

% In diesen channel wird das Delta_Tu geschrieben
writeChannelID = 383152;
writeAPIKey = 'ZM2ZQ0XMTDWH1RB9';

% Die letzten 2 Temperaturwerte aus dem channel 'motor_1' lesen
tu = thingSpeakRead(readChannelID, 'Fields', TuFieldID, 'NumPoints', 2, 'ReadKey', readAPIKey);

% Wenn mindestens zwei Werte vorhanden sind,
% Differenz ausrechnen und in neuen channel schreiben
if length(tu) > 1
    delta_Tu = tu(2)-tu(1);
    display(delta_Tu, 'Temperaturänderung')
    thingSpeakWrite(writeChannelID, delta_Tu, 'writekey', writeAPIKey);
end

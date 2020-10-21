INSERT INTO configurations_configuration(name, compare, range_min, range_max, duration, version)
VALUES 
    ("HR", 0, 200, 0, 15, 1),    /* Any heart rate >200 beats per minute (BPM) SEND Alert after 15 seconds */
    ("HR", 1, 0, 40, 15, 1),     /* BPM < 40 for 15 seconds SEND ALERT. */
    ("HR", 2, 147, 153, 300, 1), /* Heart rates that are between 147 BPM and 153 for 5 minutes SEND ALERT */
    ("HR", 1, 0, 1, 5, 1),       /* Detect a pause in heart rate; that is no beat for 5 seconds; SEND Alarm */
    ("TEM", 0, 38, 0, 300, 1),   /* TEMPERATURE >38C ==> ALERT (after 300s) */
    ("TEM", 1, 0, 35, 300, 1),   /* TEMPERATURE < 35C ==> ALERT after (300s) */
    ("O2S", 1, 0, 0.99, 60, 1),  /* O2 saturation should be typically at 99% ANYTHING < 90% merits an ALERT after 60s */
    ("RR", 0, 25, 0, 120, 1),    /* Respiratory Rate (RR) > 25 */ 
    ("RR", 0, 30, 0, 60, 1);     /* In all cases RR > 30 for 60 seconds warrants an ALERT */
.quit
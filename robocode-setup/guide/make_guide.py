"""Build ROBOCODE_SETUP_GUIDE.pdf for the frozen ESP-Drone setup."""
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

OUT = sys.argv[1]

NAVY = colors.HexColor('#1F3A5F')
BLUE = colors.HexColor('#2E6DB4')
GREY_BG = colors.HexColor('#F2F4F7')
GREY_LINE = colors.HexColor('#D0D5DD')
GREEN = colors.HexColor('#2E7D32')
GREEN_BG = colors.HexColor('#EAF5EA')
AMBER = colors.HexColor('#B26A00')
AMBER_BG = colors.HexColor('#FFF4E0')
RED = colors.HexColor('#B3261E')
RED_BG = colors.HexColor('#FDECEA')

ss = getSampleStyleSheet()
BODY = ParagraphStyle('body', parent=ss['Normal'], fontName='Helvetica', fontSize=10.5,
                      leading=14.5, spaceAfter=5, alignment=TA_LEFT)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=9, leading=12, textColor=colors.HexColor('#475467'))
TITLE = ParagraphStyle('title', parent=BODY, fontName='Helvetica-Bold', fontSize=26, leading=31,
                       textColor=NAVY, spaceAfter=6)
SUBTITLE = ParagraphStyle('subtitle', parent=BODY, fontSize=13, leading=17, textColor=BLUE, spaceAfter=14)
H1 = ParagraphStyle('h1', parent=BODY, fontName='Helvetica-Bold', fontSize=17, leading=21,
                    textColor=NAVY, spaceBefore=4, spaceAfter=8, keepWithNext=1)
H2 = ParagraphStyle('h2', parent=BODY, fontName='Helvetica-Bold', fontSize=12.5, leading=16,
                    textColor=BLUE, spaceBefore=10, spaceAfter=4, keepWithNext=1)
STEP_NUM = ParagraphStyle('stepnum', parent=BODY, fontName='Helvetica-Bold', textColor=colors.white,
                          alignment=1, fontSize=10.5, leading=13)
CELL = ParagraphStyle('cell', parent=BODY, fontSize=9.5, leading=12.5, spaceAfter=0)
CELL_B = ParagraphStyle('cellb', parent=CELL, fontName='Helvetica-Bold')
CODE = ParagraphStyle('code', fontName='Courier', fontSize=9.5, leading=12.5)

W = A4[0] - 36 * mm  # usable width


def p(text, style=BODY):
    return Paragraph(text, style)


def code(text):
    t = Table([[Preformatted(text.strip('\n'), CODE)]], colWidths=[W - 8 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GREY_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, GREY_LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def box(kind, text):
    colour, bg, label = {
        'check': (GREEN, GREEN_BG, 'CHECK'),
        'note': (BLUE, colors.HexColor('#EAF1FB'), 'NOTE'),
        'warn': (AMBER, AMBER_BG, 'IMPORTANT'),
        'danger': (RED, RED_BG, 'SAFETY'),
    }[kind]
    content = Paragraph(f'<font color="{colour.hexval().replace("0x", "#")}"><b>{label}</b></font>&nbsp;&nbsp;{text}', CELL)
    t = Table([['', content]], colWidths=[3 * mm, W - 11 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colour), ('BACKGROUND', (1, 0), (1, 0), bg),
        ('LEFTPADDING', (1, 0), (1, 0), 8), ('RIGHTPADDING', (1, 0), (1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def step(n, title, *items):
    """A numbered step: bold title, then paragraphs / code / boxes."""
    inner = [p(f'<b>{title}</b>', BODY)]
    for it in items:
        inner.append(p(it) if isinstance(it, str) else it)
        inner.append(Spacer(1, 2))
    num = Table([[Paragraph(str(n), STEP_NUM)]], colWidths=[7 * mm], rowHeights=[7 * mm])
    num.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BLUE),
                             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                             ('ROUNDEDCORNERS', [3, 3, 3, 3])]))
    t = Table([[num, inner]], colWidths=[10 * mm, W - 10 * mm])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return t


def table(rows, widths, header=True):
    data = [[Paragraph(c, CELL_B if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [('GRID', (0, 0), (-1, -1), 0.5, GREY_LINE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
          ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
    if header:
        st.append(('BACKGROUND', (0, 0), (-1, 0), GREY_BG))
    t.setStyle(TableStyle(st))
    return t


def on_page(c, doc):
    c.saveState()
    c.setFont('Helvetica', 8.5)
    c.setFillColor(colors.HexColor('#667085'))
    c.drawString(18 * mm, 10 * mm, 'Robocode UK  |  ESP-Drone Setup Guide  |  ESP-IDF 5.0.7, ESP32-S2 / S3')
    c.drawRightString(A4[0] - 18 * mm, 10 * mm, f'Page {doc.page}')
    c.setStrokeColor(GREY_LINE)
    c.line(18 * mm, 13 * mm, A4[0] - 18 * mm, 13 * mm)
    c.restoreState()


S = []

# ---------------------------------------------------------------- cover / overview
S += [
    Spacer(1, 6 * mm),
    p('ESP-Drone Setup Guide', TITLE),
    p('From a fresh Windows PC to a flashed drone streaming live data to cfclient', SUBTITLE),
    p('This guide sets up the <b>Robocode frozen version</b> of ESP-Drone. Every part is pinned to an '
      'exact, tested version, so it works the same today and next year. Parts A and B are done '
      '<b>once per PC</b>; everything you need for them is in one folder of the code, '
      '<font face="Courier">robocode-setup</font>.'),
    Spacer(1, 4),
    table([
        ['Part', 'What you do', 'Time'],
        ['A', 'Download the Robocode ESP-Drone code', '5 min'],
        ['B', 'Double-click <b>SETUP.bat</b>: it installs Git, ESP-IDF 5.0.7, Python 3.11 and cfclient', '20-40 min'],
        ['C', 'Build the firmware and flash it to the drone', '10 min'],
        ['D', 'Connect to the drone and check live data in cfclient', '5 min'],
        ['E', 'Troubleshooting', 'as needed'],
    ], [14 * mm, W - 44 * mm, 30 * mm]),
    Spacer(1, 8),
    p('What you need', H2),
    table([
        ['Item', 'Notes'],
        ['Windows 10 or 11 PC', 'With internet (setup downloads about 1 GB) and permission to install software.'],
        ['ESP-Drone (ESP32-S2 or ESP32-S3)', 'The Robocode drones are ESP32-S2. Battery charged.'],
        ['USB cable', 'Must be a <b>data</b> cable (some phone-charging cables are power-only).'],
        ['Access to the code', 'A GitHub account with access to <b>RobocodeUK/esp-drone-idf5</b>, '
                               'or a copy of the folder from your teacher.'],
        ['Gamepad (optional)', 'For flying from cfclient, e.g. a PS3/PS4/Xbox USB controller.'],
    ], [52 * mm, W - 52 * mm]),
    Spacer(1, 8),
    p('What is in the robocode-setup folder', H2),
    table([
        ['File', 'What it is'],
        ['<b>SETUP.bat</b>', 'Double-click this. Installs everything below that the PC is missing.'],
        ['ROBOCODE_SETUP_GUIDE.pdf', 'This guide.'],
        ['install_cfclient.bat', 'Installs or repairs just cfclient (SETUP.bat runs it for you).'],
        ['DOWNLOAD_LINKS.txt', 'The exact installer links and their fingerprints, if you ever need them by hand.'],
        ['downloads', 'Created by SETUP.bat. Holds the downloaded installers; can be deleted afterwards.'],
    ], [52 * mm, W - 52 * mm]),
    PageBreak(),
]

# ---------------------------------------------------------------- Part A
S += [
    p('Part A - Download the code (once per PC)', H1),
    p('Use <b>one</b> of these two options. Both end with the code in '
      '<font face="Courier">C:\\esp\\esp-drone-idf5</font>.'),
    step(1, 'Option 1 - Download ZIP (no extra software needed)',
         '&bull; Go to <b>github.com/RobocodeUK/esp-drone-idf5</b> and sign in.<br/>'
         '&bull; Click the green <b>Code</b> button, then <b>Download ZIP</b>.<br/>'
         '&bull; Create the folder <font face="Courier">C:\\esp</font>.<br/>'
         '&bull; Right-click the downloaded ZIP, choose <b>Extract All</b>, and extract it into '
         '<font face="Courier">C:\\esp</font>.<br/>'
         '&bull; Rename the new folder <font face="Courier">esp-drone-idf5-main</font> to '
         '<font face="Courier">esp-drone-idf5</font>.'),
    step(2, 'Option 2 - Git clone (if Git is already installed)',
         'Open <b>Command Prompt</b> and run these three commands:',
         code('mkdir C:\\esp\n'
              'cd C:\\esp\n'
              'git clone https://github.com/RobocodeUK/esp-drone-idf5.git')),
    box('check', 'This file must exist: <font face="Courier">C:\\esp\\esp-drone-idf5\\robocode-setup\\SETUP.bat</font>. '
                 'If it is one folder deeper (e.g. <font face="Courier">esp-drone-idf5\\esp-drone-idf5-main\\...</font>), '
                 'move the files up so the path matches. Keep this exact short path: long paths or paths with '
                 'spaces cause build errors on Windows.'),
    Spacer(1, 4),
    p('Part B - Run SETUP.bat (once per PC)', H1),
    step(1, 'Start the setup',
         'In File Explorer open <font face="Courier">C:\\esp\\esp-drone-idf5\\robocode-setup</font> and '
         'double-click <b>SETUP.bat</b>. Read the first screen and press any key to start. '
         'It works through three stages and skips anything the PC already has:',
         '&bull; <b>[1/3] Git for Windows</b> - downloaded and installed automatically.<br/>'
         '&bull; <b>[2/3] ESP-IDF 5.0.7</b> - downloads the 916 MB installer, then opens its window (see step 2).<br/>'
         '&bull; <b>[3/3] Python 3.11 and cfclient</b> - installed automatically, plus a '
         '<b>cfclient (ESP-Drone)</b> shortcut on the desktop.',
         box('note', 'When Windows asks <i>Do you want to allow this app to make changes?</i>, click <b>Yes</b>. '
                     'Every download is checked against a fingerprint before it runs; if a file does not match, '
                     'SETUP.bat deletes it and stops.')),
    step(2, 'Click through the ESP-IDF installer window',
         'When the ESP-IDF installer opens:',
         '&bull; Keep the default install folder <font face="Courier">C:\\Espressif</font>.<br/>'
         '&bull; If it offers to <b>apply fixes</b> (e.g. long path support), accept.<br/>'
         '&bull; Leave the <b>drivers</b> ticked (Silicon Labs CP210x, FTDI, Espressif USB) and the target chips '
         'ticked. The drivers let Windows talk to the drone over USB.<br/>'
         '&bull; Click <b>Install</b>, wait 15-30 minutes, then click <b>Finish</b>. SETUP.bat carries on by itself.'),
    step(3, 'Wait for "Setup complete"',
         box('check', 'The SETUP.bat window ends with <b>Setup complete</b>. You now have an '
                      '<b>ESP-IDF 5.0 CMD</b> shortcut in the Start menu and a <b>cfclient (ESP-Drone)</b> shortcut on '
                      'the desktop. You can delete the <font face="Courier">downloads</font> folder to free about 1 GB.'),
         box('note', 'If it says <b>Setup FAILED</b>, read the message above it, fix the problem (often the internet '
                     'connection, or clicking No on a permission prompt) and run SETUP.bat again. Finished stages '
                     'are skipped.')),
    Spacer(1, 6),
]

# ---------------------------------------------------------------- Part C
S += [
    p('Part C - Build and flash the firmware', H1),
    box('warn', 'Always build and flash from the <b>ESP-IDF 5.0 CMD</b> shortcut in the Start menu. A normal '
                'Command Prompt or PowerShell window does not have the tools set up and will show errors.'),
    Spacer(1, 6),
    step(1, 'Plug in the drone and find its COM port',
         'Connect the drone to the PC with the USB data cable. Open <b>Device Manager</b> '
         '(right-click Start) and expand <b>Ports (COM &amp; LPT)</b>. Look for '
         '<b>Silicon Labs CP210x USB to UART Bridge (COM3)</b>. The number (here <b>COM3</b>) is your port.',
         box('note', 'If no new port appears: try another USB cable (it may be power-only) or another USB socket. '
                     'Unplug and replug the drone and watch which entry appears.')),
    step(2, 'Open ESP-IDF 5.0 CMD and go to the code folder',
         code('cd C:\\esp\\esp-drone-idf5')),
    step(3, 'Check which chip the drone has (ESP32-S2 or ESP32-S3)',
         'Replace COM3 with your port:',
         code('python -m esptool -p COM3 chip_id'),
         'Look for the line <font face="Courier">Chip is ESP32-S2</font> or '
         '<font face="Courier">Chip is ESP32-S3</font>.'),
    step(4, 'Select the chip type',
         'For ESP32-S2 (the Robocode drones):',
         code('idf.py set-target esp32s2'),
         'For ESP32-S3 use <font face="Courier">idf.py set-target esp32s3</font> instead. You only need to do '
         'this again if you switch to a drone with the other chip.'),
    step(5, 'Build, flash and watch the drone start up',
         code('idf.py -p COM3 flash monitor'),
         'The first build takes 5-10 minutes; later builds are much faster. When flashing finishes, the '
         'drone restarts and its log scrolls in the window.',
         box('check', 'In the log you should see <font face="Courier">MPU6050 I2C connection [OK]</font> and, '
                      'after the drone has been kept still for a few seconds, '
                      '<font face="Courier">STAB: Ready to fly.</font> '
                      'Lines saying VL53L1X, Z-down or PMW3901 <b>[FAIL]</b> are normal: those are optional add-on '
                      'sensors that are not fitted.'),
         'Press <b>Ctrl + ]</b> to leave the monitor. The drone is now flashed.'),
    Spacer(1, 6),
]

# ---------------------------------------------------------------- Part D
S += [
    p('Part D - Connect to the drone', H1),
    box('danger', 'For first tests, <b>remove the propellers</b> or hold the drone firmly. When a gamepad is '
                  'connected, moving the thrust stick spins the motors.'),
    Spacer(1, 6),
    step(1, 'Power on the drone and keep it still',
         'Connect the battery (USB is not needed for flying). Put the drone on a flat surface and do not '
         'touch it for about 10 seconds while it calibrates its sensors.'),
    step(2, 'Connect the PC to the drone\'s Wi-Fi',
         'In the Windows Wi-Fi list, choose <b>ESP-DRONE_XXXXXXXXXXXX</b> (each drone has its own number) '
         'and enter the password <font face="Courier"><b>12345678</b></font>. Windows will say '
         '<i>No internet</i>; that is normal.',
         box('warn', 'Windows may switch back to your normal Wi-Fi after about 40 seconds because the drone has no '
                     'internet, which cuts off cfclient. To stop this, go to <b>Settings &gt; Network &amp; '
                     'internet &gt; Wi-Fi &gt; Manage known networks</b>, click your normal network and untick '
                     '<b>Connect automatically when in range</b>. Turn it back on when you finish.')),
    step(3, 'Open cfclient and connect',
         'If you are using a gamepad, plug it in <b>before</b> opening cfclient. Start <b>cfclient (ESP-Drone)</b> '
         'from the desktop. Click <b>Scan</b>, choose <font face="Courier">udp://192.168.43.42:2390</font> in '
         'the list next to it, then click <b>Connect</b>.',
         box('check', 'On the <b>Flight Control</b> tab, roll, pitch and yaw update live. Tilt the drone gently by '
                      'hand and the numbers and horizon should follow it, and keep following it for minutes. '
                      'The drone\'s green LED blinks quickly while connected.')),
    step(4, 'Set up a gamepad (optional)',
         'Menu <b>Input device</b>: select your controller, then choose a mapping (for a PS3/PS4 pad, '
         '<b>PS3_Mode_1</b> is a good start). Use <b>Input device &gt; Configure device mapping</b> to change it. '
         'Keep the thrust stick fully down when connecting.'),
    step(5, 'Finish',
         'Click <b>Disconnect</b> in cfclient, unplug the drone battery, and reconnect the PC to your normal '
         'Wi-Fi.'),
    Spacer(1, 8),
]

# ---------------------------------------------------------------- Part E troubleshooting
S += [
    p('Part E - Troubleshooting', H1),
    table([
        ['Problem', 'Fix'],
        ['SETUP.bat: <i>download failed</i> or <i>does not match the expected fingerprint</i>',
         'Check the internet connection and run SETUP.bat again (downloads resume). If the fingerprint still '
         'does not match, do not install the file by hand; tell your teacher.'],
        ['SETUP.bat: <i>Git did not install</i> or <i>ESP-IDF 5.0.7 was not found</i>',
         'You probably clicked <b>No</b> on a permission prompt, or changed the ESP-IDF install folder. Run '
         'SETUP.bat again, click <b>Yes</b>, and keep <font face="Courier">C:\\Espressif</font>.'],
        ['<font face="Courier">\'idf.py\' is not recognized</font>, or errors like <i>tool xtensa... has no '
         'installed versions</i> / <i>python_env ... doesn\'t exist</i>',
         'You are in a normal Command Prompt. Open <b>ESP-IDF 5.0 CMD</b> from the Start menu and try again.'],
        ['No COM port appears for the drone',
         'Use a different (data) USB cable or USB socket. If it still does not appear, run the ESP-IDF installer '
         'from the <font face="Courier">downloads</font> folder again and make sure the <b>drivers</b> are ticked.'],
        ['Flashing fails: <i>Failed to connect</i> or <i>Access is denied</i>',
         'Close anything else using the port (another monitor window, Arduino IDE). Check the COM number. '
         'If it still fails, hold the <b>BOOT</b> button on the drone board while the flash starts.'],
        ['Drone log shows <font face="Courier">MPU6050 I2C connection [FAIL]</font>. cfclient connects '
         'but the data never moves',
         'The motion sensor has locked up (common after a crash or on a low battery). Unplug <b>both</b> the '
         'USB cable and the battery, wait 10 seconds, then power on again. Charge the battery.'],
        ['cfclient data freezes after about 40 seconds',
         'Windows switched back to your normal Wi-Fi. See the <b>IMPORTANT</b> box in Part D step 2.'],
        ['cfclient data freezes after only a few seconds, or cfclient will not start',
         'Repair it: double-click <b>install_cfclient.bat</b> in the robocode-setup folder.'],
        ['cfclient: <i>Socket is already connected</i> or will not reconnect',
         'Close cfclient completely and open it again.'],
        ['Scan / Connect does nothing',
         'Check the PC is connected to the drone\'s Wi-Fi (not your normal network) and the drone is powered.'],
        ['Build errors mentioning long paths or missing files',
         'Make sure the code is at exactly <font face="Courier">C:\\esp\\esp-drone-idf5</font> (no spaces).'],
    ], [70 * mm, W - 70 * mm]),
    Spacer(1, 10),
    KeepTogether([
    p('For teachers: keeping the setup frozen', H2),
    p('Everything is pinned so nothing changes unless Robocode changes it:',
      ParagraphStyle('keep', parent=BODY, keepWithNext=1)),
    table([
        ['Part', 'Pinned to'],
        ['Firmware', '<b>RobocodeUK/esp-drone-idf5</b> (based on Espressif esp-drone commit db0f6562, the last '
                     'version for ESP-IDF 5.0). esp-now 2.5.2 is included in the code, so nothing is downloaded '
                     'at build time.'],
        ['Installers', 'Git 2.47.1, ESP-IDF 5.0.7 offline, Python 3.11.9 - official links with SHA-256 '
                       'fingerprints in <font face="Courier">robocode-setup\\DOWNLOAD_LINKS.txt</font>'],
        ['cfclient', '<b>RobocodeUK/crazyflie-clients-python</b>, commit 76d5093'],
        ['cflib (drone link)', '<b>RobocodeUK/crazyflie-lib-python</b>, commit f2baeab (adds the Wi-Fi keep-alive fix)'],
        ['Python libraries', 'Exact versions in <font face="Courier">robocode-setup\\requirements-cfclient.txt</font>'],
    ], [38 * mm, W - 38 * mm]),
    Spacer(1, 6),
    p('&bull; Do not update to Espressif\'s latest esp-drone: it needs ESP-IDF 5.5 or 6.1.<br/>'
      '&bull; To get Robocode updates later, download the ZIP again (or run <font face="Courier">git pull</font>), '
      'then run <b>install_cfclient.bat</b>.<br/>'
      '&bull; More details are in <font face="Courier">ROBOCODE_README.md</font> in the code folder.'),
    ]),
]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=16 * mm, bottomMargin=18 * mm,
                        title='ESP-Drone Setup Guide', author='Robocode UK',
                        subject='ESP-Drone with ESP-IDF 5.0.7 and cfclient')
doc.build(S, onFirstPage=on_page, onLaterPages=on_page)
print('wrote', OUT)

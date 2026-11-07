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
      'exact, tested version, so it works the same today and next year. Follow the parts in order; '
      'Parts A, B and D are done <b>once per PC</b>.'),
    Spacer(1, 4),
    table([
        ['Part', 'What you do', 'Time'],
        ['A', 'Install the tools: Git and ESP-IDF 5.0.7', '25-40 min'],
        ['B', 'Download the Robocode ESP-Drone code', '2 min'],
        ['C', 'Build the firmware and flash it to the drone', '10 min'],
        ['D', 'Install cfclient (PC app to view data and fly) - one double-click, also sets up Python', '5-10 min'],
        ['E', 'Connect to the drone and check live data', '5 min'],
        ['F', 'Troubleshooting', 'as needed'],
    ], [14 * mm, W - 44 * mm, 30 * mm]),
    Spacer(1, 8),
    p('What you need', H2),
    table([
        ['Item', 'Notes'],
        ['Windows 10 or 11 PC', 'With internet for Parts A, B and D. Admin rights to install software.'],
        ['ESP-Drone (ESP32-S2 or ESP32-S3)', 'The Robocode drones are ESP32-S2. Battery charged.'],
        ['USB cable', 'Must be a <b>data</b> cable (some phone-charging cables are power-only).'],
        ['Access to the code', 'A GitHub account with access to <b>RobocodeUK/esp-drone-idf5</b>, '
                               'or a copy of the folder from your teacher.'],
        ['Gamepad (optional)', 'For flying from cfclient, e.g. a PS3/PS4/Xbox USB controller.'],
    ], [52 * mm, W - 52 * mm]),
    Spacer(1, 8),
    box('warn', 'Use exactly <b>ESP-IDF 5.0.7</b>: newer versions will not build this code. cfclient needs '
                '<b>Python 3.11</b>; the cfclient installer in Part D sets this up for you, so you do not need to '
                'install Python yourself. Do not download ESP-Drone from Espressif\'s GitHub; use the Robocode copy.'),
    PageBreak(),
]

# ---------------------------------------------------------------- Part A
S += [
    p('Part A - Install the tools (once per PC)', H1),
    step(1, 'Install Git for Windows',
         'Go to <b>git-scm.com/download/win</b>, download the 64-bit installer and run it. '
         'Click <b>Next</b> on every page to accept the defaults, then <b>Install</b>.',
         box('check', 'Open <b>Command Prompt</b> (Start menu, type <i>cmd</i>) and run '
                      '<font face="Courier">git --version</font>. It should print a version number.')),
    step(2, 'Install ESP-IDF 5.0.7 (the ESP32 build tools)',
         'Go to <b>dl.espressif.com/dl/esp-idf/</b> and download the <b>ESP-IDF v5.0.7 Offline Installer</b> '
         '(file name similar to <font face="Courier">esp-idf-tools-setup-offline-5.0.7.exe</font>, about 1 GB). '
         'Run it and:',
         '&bull; Keep the default install folder <font face="Courier">C:\\Espressif</font>.<br/>'
         '&bull; If it offers to <b>apply fixes</b> (e.g. long path support), accept.<br/>'
         '&bull; On the components page, leave the <b>drivers</b> ticked (Silicon Labs CP210x, FTDI, '
         'Espressif USB). These let Windows talk to the drone over USB.<br/>'
         '&bull; Leave the target chips ticked (at least ESP32-S2 and ESP32-S3).',
         'Installation takes 15-30 minutes. At the end it adds Start menu shortcuts called '
         '<b>ESP-IDF 5.0 CMD</b> and <b>ESP-IDF 5.0 PowerShell</b>.',
         box('check', 'Open <b>ESP-IDF 5.0 CMD</b> from the Start menu and run '
                      '<font face="Courier">idf.py --version</font>. It should print <b>ESP-IDF v5.0.7</b>.'),
         box('warn', 'Always build and flash from the <b>ESP-IDF 5.0 CMD</b> shortcut. A normal Command Prompt '
                     'or PowerShell window does not have the tools set up and will show errors.')),
    Spacer(1, 6),
]

# ---------------------------------------------------------------- Part B
S += [
    p('Part B - Download the code (once per PC)', H1),
    step(1, 'Clone the code into C:\\esp\\esp-drone',
         'Open <b>Command Prompt</b> and run these two commands:',
         code('mkdir C:\\esp\n'
              'git clone https://github.com/RobocodeUK/esp-drone-idf5.git C:\\esp\\esp-drone'),
         'The first time, a GitHub sign-in window may appear. Sign in with the account that has '
         'access to RobocodeUK.',
         box('note', 'No GitHub access? Ask your teacher for a copy of the <b>esp-drone</b> folder and put it at '
                     '<font face="Courier">C:\\esp\\esp-drone</font>. Keep this exact short path: long paths or '
                     'paths with spaces cause build errors on Windows.')),
    Spacer(1, 4),
    p('Part C - Build and flash the firmware', H1),
    step(1, 'Plug in the drone and find its COM port',
         'Connect the drone to the PC with the USB data cable. Open <b>Device Manager</b> '
         '(right-click Start) and expand <b>Ports (COM &amp; LPT)</b>. Look for '
         '<b>Silicon Labs CP210x USB to UART Bridge (COM3)</b>. The number (here <b>COM3</b>) is your port.',
         box('note', 'If no new port appears: try another USB cable (it may be power-only) or another USB socket. '
                     'Unplug and replug the drone and watch which entry appears.')),
    step(2, 'Open ESP-IDF 5.0 CMD and go to the code folder',
         code('cd C:\\esp\\esp-drone')),
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

# ---------------------------------------------------------------- Part D / E
S += [
    p('Part D - Install cfclient (once per PC)', H1),
    step(1, 'Run the installer',
         'cfclient is the PC app for viewing the drone\'s live sensor data and flying it with a gamepad. '
         'In File Explorer open <font face="Courier">C:\\esp\\esp-drone\\tools\\cfclient</font> and '
         'double-click <b>install_cfclient.bat</b>. It works through four stages:',
         '&bull; <b>[1/4]</b> Checks for Python 3.11. If this PC does not have it, it downloads '
         '<b>Python 3.11.9</b> from python.org and installs it for your Windows user (no admin needed, '
         'and any other Python versions are left alone).<br/>'
         '&bull; <b>[2/4]</b> Checks Git is installed.<br/>'
         '&bull; <b>[3/4]</b> Installs cfclient with the exact tested versions of everything.<br/>'
         '&bull; <b>[4/4]</b> Adds a <b>cfclient (ESP-Drone)</b> shortcut to the desktop.',
         'It takes 5-10 minutes. Leave the window open until it finishes.',
         box('check', 'The window ends with <b>Done</b> and the <b>cfclient (ESP-Drone)</b> shortcut is on the '
                      'desktop. Press any key to close the window.'),
         box('note', 'If it says <i>Git not found</i>, install Git (Part A step 1) and run it again. '
                     'It is safe to run the installer again at any time.')),
    Spacer(1, 4),
    p('Part E - Connect to the drone', H1),
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

# ---------------------------------------------------------------- Part F troubleshooting
S += [
    p('Part F - Troubleshooting', H1),
    table([
        ['Problem', 'Fix'],
        ['<font face="Courier">\'idf.py\' is not recognized</font>, or errors like <i>tool xtensa... has no '
         'installed versions</i> / <i>python_env ... doesn\'t exist</i>',
         'You are in a normal Command Prompt. Open <b>ESP-IDF 5.0 CMD</b> from the Start menu and try again.'],
        ['No COM port appears for the drone',
         'Use a different (data) USB cable or USB socket. If it still does not appear, re-run the ESP-IDF '
         'installer and make sure the <b>drivers</b> are ticked.'],
        ['Flashing fails: <i>Failed to connect</i> or <i>Access is denied</i>',
         'Close anything else using the port (another monitor window, Arduino IDE). Check the COM number. '
         'If it still fails, hold the <b>BOOT</b> button on the drone board while the flash starts.'],
        ['Drone log shows <font face="Courier">MPU6050 I2C connection [FAIL]</font>. cfclient connects '
         'but the data never moves',
         'The motion sensor has locked up (common after a crash or on a low battery). Unplug <b>both</b> the '
         'USB cable and the battery, wait 10 seconds, then power on again. Charge the battery.'],
        ['cfclient data freezes after about 40 seconds',
         'Windows switched back to your normal Wi-Fi. See the <b>IMPORTANT</b> box in Part E step 2.'],
        ['cfclient data freezes after only a few seconds',
         'You have an old cfclient install. Re-run <b>install_cfclient.bat</b> (Part D).'],
        ['cfclient: <i>Socket is already connected</i> or will not reconnect',
         'Close cfclient completely and open it again.'],
        ['Scan / Connect does nothing',
         'Check the PC is connected to the drone\'s Wi-Fi (not your normal network) and the drone is powered.'],
        ['install_cfclient.bat: <i>Git not found</i>',
         'Install Git for Windows (Part A step 1), then run it again.'],
        ['install_cfclient.bat fails at step [1/4] (Python download or install)',
         'Check the internet connection and run it again. If it still fails, install <b>Python 3.11.9</b> '
         'yourself from <b>python.org/downloads/release/python-3119/</b> (Windows installer 64-bit) and run '
         'the .bat again; it will find it.'],
        ['Build errors mentioning long paths or missing files',
         'Make sure the code is at exactly <font face="Courier">C:\\esp\\esp-drone</font> (no spaces).'],
    ], [70 * mm, W - 70 * mm]),
    Spacer(1, 10),
    p('For teachers: keeping the setup frozen', H2),
    p('Everything is pinned so nothing changes unless Robocode changes it:',
      ParagraphStyle('keep', parent=BODY, keepWithNext=1)),
    table([
        ['Part', 'Pinned to'],
        ['Firmware', '<b>RobocodeUK/esp-drone-idf5</b> (based on Espressif esp-drone commit db0f6562, the last '
                     'version for ESP-IDF 5.0). esp-now 2.5.2 is included in the code, so nothing is downloaded '
                     'at build time.'],
        ['cfclient', '<b>RobocodeUK/crazyflie-clients-python</b>, commit 76d5093'],
        ['cflib (drone link)', '<b>RobocodeUK/crazyflie-lib-python</b>, commit f2baeab (adds the Wi-Fi keep-alive fix)'],
        ['Python libraries', 'Exact versions in <font face="Courier">tools\\cfclient\\requirements-cfclient.txt</font>'],
        ['Tools', 'ESP-IDF 5.0.7, Python 3.11.9'],
    ], [38 * mm, W - 38 * mm]),
    Spacer(1, 6),
    p('&bull; Do not update to Espressif\'s latest esp-drone: it needs ESP-IDF 5.5 or 6.1.<br/>'
      '&bull; To get Robocode updates later, run <font face="Courier">git pull</font> inside '
      '<font face="Courier">C:\\esp\\esp-drone</font>, then re-run <b>install_cfclient.bat</b>.<br/>'
      '&bull; More details are in <font face="Courier">ROBOCODE_README.md</font> in the code folder.'),
]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=16 * mm, bottomMargin=18 * mm,
                        title='ESP-Drone Setup Guide', author='Robocode UK',
                        subject='ESP-Drone with ESP-IDF 5.0.7 and cfclient')
doc.build(S, onFirstPage=on_page, onLaterPages=on_page)
print('wrote', OUT)

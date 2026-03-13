"""
Script khusus device: ACP250929NBUC1VX
Single-run: install → launch → create wallet → get seed phrase OTP → selesai
Semua koordinat hardcoded, resolusi 1080x1920 DPI 320.
"""

import requests, time, json, logging, sys, re, random, string
from datetime import datetime
from logging.handlers import RotatingFileHandler
import glob, os

# ============================================================
# KONFIGURASI
# ============================================================

EMAIL         = "@gmail.com"
PASSWORD_MD5  = ""
BASE          = "https://api.vsphone.com/vsphone/api"
TARGET_PKG    = "com.ant.dt.topnod"

PAD_CODE      = "ACP250929NBUC1VX"
DEVICE_NAME   = "ACP250929NBUC1VX"

REFERRAL_CODE   = "ISIREF"
WALLET_PASSWORD = "masuk123"
OTP_TIMEOUT     = 180
LAUNCH_WAIT     = 25
FACTORY_RESET_WAIT = 120
INSTALL_TIMEOUT = 20

MAILTM_PASS = "zays12345"

# ============================================================
# KOORDINAT UI
# ============================================================

WALLET_TAB         = (945, 1809)
CREATE_WALLET_BTN  = (540, 1629)
AGREE_TERMS_BTN    = (540, 1788)
EMAIL_FIELD        = (528,  476)
OTP_FIELD          = (496,  660)
SEND_OTP_BTN       = (979,  660)
REFF_DROPDOWN      = (540,  770)
REFF_FIELD         = (528,  848)
NEXT_BUTTON        = (540,  948)
NEXT_BUTTON_KB     = (540, 1036)
PASS_FIELD         = (504,  578)
CONFIRM_PASS_KB    = (504,  606)
AGREE_FORGET_CB    = (58,  1636)
FINAL_CONTINUE     = (540, 1768)
GOOGLE_SAVE_CANCEL = (250, 2050)
SKIP_BIOMETRIC     = (1001,  90)
SET_UP_LATER       = (540, 1772)

SETTINGS_BTN          = (72,    96)
SHOW_RECOVERY_PHRASE  = (540, 1291)
RISK_WARNING_CONFIRM  = (795, 1772)
SEED_OTP_FIELD        = (447, 1576)
SEED_OTP_CONFIRM      = (540, 1764)
SEED_PASS_FIELD       = (504,  578)
SEED_CONTINUE_BTN     = (540, 1768)

D = {
    "after_tap_wallet_tab":    6,
    "after_agree_checkbox":    3,
    "after_create_wallet_btn": 6,
    "after_agree_terms_btn":   6,
    "after_tap_email_field":   3,
    "after_type_email":        3,
    "after_send_otp":          5,
    "after_tap_otp_field":     3,
    "after_type_otp":          3,
    "after_tap_reff_dropdown": 4,
    "after_tap_reff_field":    3,
    "after_type_reff":         3,
    "after_next_button":       8,
    "after_tap_pass_field":    3,
    "after_type_password":     3,
    "after_tap_confirm_pass":  3,
    "after_hide_keyboard":     3,
    "after_agree_forget_cb":   3,
    "after_final_continue":    9,
    "after_google_save_cancel":5,
    "after_skip_biometric":    5,
    "after_set_up_later":      4,
}

# ============================================================
# WARNA & TAMPILAN CLI
# ============================================================

class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RED    = "\033[31m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    BLUE   = "\033[34m"
    PURPLE = "\033[35m"
    CYAN   = "\033[36m"
    WHITE  = "\033[37m"

W = 58

def _strip_ansi(s: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", s)

def box_top(title: str = "", color: str = C.CYAN):
    if title:
        pad   = W - len(title) - 4
        left  = pad // 2
        right = pad - left
        print(f"{color}{C.BOLD}╔{'═'*(left+1)} {title} {'═'*(right+1)}╗{C.RESET}")
    else:
        print(f"{color}{C.BOLD}╔{'═'*(W+2)}╗{C.RESET}")

def box_mid(text: str = "", color: str = C.CYAN, text_color: str = C.WHITE):
    inner = f"  {text}"
    pad   = W - len(_strip_ansi(inner))
    print(f"{color}{C.BOLD}║{C.RESET}{text_color}{inner}{' '*max(pad,0)}{C.RESET}{color}{C.BOLD}║{C.RESET}")

def box_bot(color: str = C.CYAN):
    print(f"{color}{C.BOLD}╚{'═'*(W+2)}╝{C.RESET}")

def section(title: str):
    print()
    print(f"  {C.BOLD}{C.CYAN}▸ {title}{C.RESET}")
    print(f"  {C.DIM}{'─'*(W-2)}{C.RESET}")

def print_ok(msg: str):   print(f"  {C.GREEN}✔{C.RESET}  {msg}")
def print_err(msg: str):  print(f"  {C.RED}✘{C.RESET}  {msg}")
def print_warn(msg: str): print(f"  {C.YELLOW}⚠{C.RESET}  {msg}")
def print_info(msg: str): print(f"  {C.CYAN}›{C.RESET}  {msg}")
def print_wait(msg: str): print(f"  {C.YELLOW}◷{C.RESET}  {msg}")
def print_run(msg: str):  print(f"  {C.PURPLE}⟳{C.RESET}  {msg}")

def countdown(seconds: int, label: str = "Lanjut dalam"):
    for i in range(seconds, 0, -5):
        print(f"\r  {C.YELLOW}◷{C.RESET}  {label} {C.BOLD}{i}s{C.RESET}...   ", end="", flush=True)
        time.sleep(min(5, i))
    print(f"\r  {C.GREEN}✔{C.RESET}  {label} {C.BOLD}0s{C.RESET}    ")

def banner():
    print()
    box_top("TopNod Single Device Bot", C.CYAN)
    box_mid(f"Device : {C.BOLD}{DEVICE_NAME}{C.RESET}", C.CYAN, "")
    box_mid(f"Mode   : Install → Wallet → Seed Phrase", C.CYAN, C.DIM)
    box_bot(C.CYAN)
    print()

# ============================================================
# LOGGING (file only — console hanya WARNING ke atas)
# ============================================================

_old_logs = sorted(glob.glob(f"device_{PAD_CODE}_log_*.txt"))
for _f in _old_logs[:-4]:
    try: os.remove(_f)
    except Exception: pass

log_filename = f"device_{PAD_CODE}_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_fh  = RotatingFileHandler(log_filename, maxBytes=2*1024*1024, backupCount=3, encoding="utf-8")
_fh.setFormatter(_fmt)
_ch  = logging.StreamHandler(sys.stdout)
_ch.setFormatter(_fmt)
_ch.setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, handlers=[_fh, _ch])
log = logging.getLogger(__name__)

# ============================================================
# SESSION
# ============================================================

session = requests.Session()
headers = {
    "Content-Type":  "application/json",
    "Clienttype":    "web",
    "Appversion":    "2003602",
    "Requestsource": "wechat-miniapp",
    "Suppliertype":  "0"
}

VCADB_ASYNC  = f"{BASE}/vcAdb/asyncAdb"
VCADB_RESULT = f"{BASE}/vcAdb/getAdbResult"

# ============================================================
# HELPERS
# ============================================================

def escape_adb(text):
    result = ""
    for ch in text:
        if ch == " ": result += "%s"
        elif ch in "\\()&|;<>!$`\"'": result += "\\" + ch
        else: result += ch
    return result

def vcadb_exec(adb_str, poll_timeout=30):
    log.info(f"ADB → {adb_str[:90]}{'...' if len(adb_str)>90 else ''}")
    r = session.post(VCADB_ASYNC,
                     json={"padCodes": [PAD_CODE], "adbStr": adb_str},
                     headers=headers, timeout=15)
    d = r.json()
    if d.get("code") != 200:
        log.warning(f"asyncAdb gagal: {d}")
        return False
    base_task_id = d["data"]
    deadline = time.time() + poll_timeout
    while time.time() < deadline:
        time.sleep(2)
        r2   = session.post(VCADB_RESULT,
                            json={"baseTaskId": base_task_id},
                            headers=headers, timeout=15)
        data = r2.json().get("data", "")
        if not data: continue
        try:
            results = json.loads(data) if isinstance(data, str) else data
            done    = {item["padCode"]: item["taskStatus"] for item in results}
            if PAD_CODE in done:
                st = done[PAD_CODE]
                log.info(f"taskStatus={st}")
                return st == 3
        except Exception as e:
            log.warning(f"parse error: {e}")
    log.warning(f"vcAdb timeout {poll_timeout}s")
    return False

def tap_by_bounds(bounds_str):
    m = re.search(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
    if not m:
        log.warning(f'tap_by_bounds invalid: {bounds_str}')
        return None
    cx = (int(m[1]) + int(m[3])) // 2
    cy = (int(m[2]) + int(m[4])) // 2
    log.info(f'tap ({cx}, {cy})')
    vcadb_exec(f'input tap {cx} {cy}', poll_timeout=15)
    return (cx, cy)

# ============================================================
# SCREENSHOT
# ============================================================

def take_screenshot(filename: str = None) -> str | None:
    try:
        r = session.post(
            f"{BASE}/padManage/padScreenshotsNew",
            json={"padCodes": [PAD_CODE]},
            headers=headers, timeout=15
        )
        data = r.json()
        if data.get("code") != 200:
            log.warning(f"Screenshot error: {data}"); return None
        access_url = next(
            (i.get("accessUrl") for i in data.get("data", []) if i.get("padCode") == PAD_CODE),
            None
        )
        if not access_url:
            log.warning("Screenshot: accessUrl tidak ditemukan"); return None
        r2 = session.get(access_url, timeout=15)
        if r2.status_code != 200:
            log.warning(f"Screenshot download error: {r2.status_code}"); return None
        if not filename:
            filename = f"screenshot_{DEVICE_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(filename, "wb") as f:
            f.write(r2.content)
        print_ok(f"Screenshot: {C.DIM}{filename}{C.RESET}")
        log.info(f"Screenshot: {filename}")
        return filename
    except Exception as e:
        log.error(f"Screenshot exception: {e}"); return None

# ============================================================
# LOGIN
# ============================================================

def login():
    section("Login")
    r = session.post(f"{BASE}/user/login",
                     json={"mobilePhone": EMAIL, "loginType": 1,
                           "password": PASSWORD_MD5, "channel": "web"},
                     headers=headers, timeout=15)
    d = r.json()
    if d.get("code") != 200:
        print_err(f"Login gagal: {d.get('msg')}")
        raise Exception(f"Login gagal: {d.get('msg')}")
    headers["token"]  = d["data"]["token"]
    headers["userid"] = str(d["data"]["userId"])
    uid = d["data"]["userId"]
    log.info(f"Login OK — UserID: {uid}")
    print_ok(f"Login berhasil  {C.DIM}UserID: {uid}{C.RESET}")

# ============================================================
# APK
# ============================================================

def get_topnod_apk():
    section("Mencari APK TopNod")
    for op in [2, 1, 3, None]:
        params = {"operType": op} if op is not None else {}
        r = session.post(f"{BASE}/cloudFile/selectFilesByUserId",
                         params=params, json={}, headers=headers, timeout=15)
        files = r.json().get("data") or []
        apks  = [f for f in files if f.get("fileType") == 2]
        for f in apks:
            if "topnod" in f.get("fileName", "").lower():
                log.info(f"APK found: {f['fileName']} id={f['fileId']}")
                print_ok(f"APK ditemukan: {C.BOLD}{f['fileName']}{C.RESET}  {C.DIM}id={f['fileId']}{C.RESET}")
                return f
        if apks:
            print_warn(f"Tidak ada APK bernama topnod. APK tersedia ({len(apks)}):")
            for i, f in enumerate(apks, 1):
                size_mb = round(f.get("fileSize", 0)/1024/1024, 1)
                print(f"    {C.CYAN}{i}.{C.RESET}  {f['fileName']}  {C.DIM}({size_mb} MB)  id={f['fileId']}{C.RESET}")
            return apks
    return None

def install_apk(apk_info):
    section("Install APK")
    task_list = [{
        "taskType":    10000,
        "padCode":     PAD_CODE,
        "equipmentId": "",
        "taskContent": json.dumps({
            "downloadUrl": apk_info["downloadUrl"],
            "fileName":    apk_info["fileName"],
            "fileType":    2,
            "fileId":      apk_info.get("fileId", 0)
        })
    }]
    r    = session.post(f"{BASE}/padTask/addPadTaskByJiGuang",
                        json={"taskList": task_list}, headers=headers, timeout=30)
    data = r.json()
    if data.get("code") != 200:
        raise Exception(f"Install gagal: {data.get('msg')}")
    tid = data["data"][0]["taskId"]
    print_wait(f"Task {C.DIM}{tid}{C.RESET} — tunggu max {INSTALL_TIMEOUT}s...")
    log.info(f"Install task {tid}")
    start = time.time()
    while time.time() - start < INSTALL_TIMEOUT:
        time.sleep(3)
        r2    = session.post(f"{BASE}/padTask/getPadTaskByTaskIds",
                             json={"taskIds": [tid]}, headers=headers, timeout=15)
        tasks = r2.json().get("data", [])
        for t in tasks:
            st = t.get("status", 0)
            if st == 2:
                log.info("Install sukses")
                print_ok("Install sukses"); return True
            if st == 3:
                log.warning("Install gagal")
                print_err("Install gagal"); return False
        sisa = INSTALL_TIMEOUT - (time.time() - start)
        print(f"\r  {C.YELLOW}◷{C.RESET}  Install berjalan...  {C.DIM}{sisa:.0f}s tersisa{C.RESET}  ", end="", flush=True)
    print()
    print_warn("Timeout install — lanjut otomatis")
    log.info("Install timeout — lanjut")
    return True

# ============================================================
# LAUNCH
# ============================================================

def launch_app():
    section("Launch TopNod")
    r = session.post(f"{BASE}/pcVersion/restartApp",
                     json={"padCodeList": [PAD_CODE], "apkPackageList": [TARGET_PKG]},
                     headers=headers, timeout=15)
    d = r.json()
    if d.get("code") == 200:
        log.info("Launch OK")
        print_ok("TopNod berhasil diluncurkan")
        countdown(LAUNCH_WAIT, "Tunggu TopNod terbuka")
        return True
    log.error(f"Launch gagal: {d}")
    print_err(f"Launch gagal: {d.get('msg', '')}")
    return False

# ============================================================
# SET RESOLUSI
# ============================================================

def set_resolution():
    section("Set Resolusi → 1080×1920, DPI 320")
    vcadb_exec("wm size 1080x1920 && wm density 320", poll_timeout=30)
    log.info("Resolusi OK")
    print_ok("Resolusi berhasil diset ke 1080×1920 DPI 320")
    time.sleep(2)

# ============================================================
# MAILTM
# ============================================================

class MailTM:
    def __init__(self):
        self.address  = None
        self.token    = None
        self.s        = requests.Session()
        self.seen_ids = set()

    def create_account(self):
        try:
            r       = self.s.get("https://api.mail.tm/domains", timeout=10)
            domains = r.json().get("hydra:member", [])
            if not domains: return False
            domain = domains[0]["domain"]
        except Exception as e:
            log.error(f"MailTM domain error: {e}"); return False

        username     = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.address = f"{username}@{domain}"
        try:
            r = self.s.post("https://api.mail.tm/accounts",
                            json={"address": self.address, "password": MAILTM_PASS}, timeout=10)
            if r.status_code == 429:
                print_warn("MailTM rate limit — retry 10s...")
                log.warning("MailTM rate limit 429")
                time.sleep(10)
                r = self.s.post("https://api.mail.tm/accounts",
                                json={"address": self.address, "password": MAILTM_PASS}, timeout=10)
            if r.status_code not in (200, 201):
                log.error(f"MailTM create error {r.status_code}")
                return False
            log.info(f"MailTM OK: {self.address}")
            return True
        except Exception as e:
            log.error(f"MailTM exception: {e}"); return False

    def get_token(self):
        try:
            r          = self.s.post("https://api.mail.tm/token",
                                     json={"address": self.address, "password": MAILTM_PASS}, timeout=10)
            self.token = r.json().get("token")
            return bool(self.token)
        except Exception as e:
            log.error(f"MailTM token error: {e}"); return False

    def wait_for_otp(self, timeout=180, keepalive_tap=None):
        if not self.token and not self.get_token(): return None
        auth     = {"Authorization": f"Bearer {self.token}"}
        deadline = time.time() + timeout
        last_tap = time.time()
        print_wait(f"Polling OTP  {C.DIM}{self.address}  (max {timeout}s){C.RESET}")
        log.info(f"MailTM polling OTP: {self.address} | seen={len(self.seen_ids)}")
        while time.time() < deadline:
            time.sleep(5)
            if keepalive_tap and (time.time() - last_tap >= 20):
                try:
                    vcadb_exec(f"input tap {keepalive_tap[0]} {keepalive_tap[1]}", poll_timeout=10)
                    last_tap = time.time()
                except Exception:
                    pass
            try:
                r        = self.s.get("https://api.mail.tm/messages", headers=auth, timeout=10)
                msgs     = r.json().get("hydra:member", [])
                new_msgs = [m for m in msgs if m["id"] not in self.seen_ids]
                if not new_msgs:
                    sisa = int(deadline - time.time())
                    print(f"\r  {C.YELLOW}◷{C.RESET}  Menunggu email...  {C.DIM}{sisa}s tersisa{C.RESET}  ", end="", flush=True)
                    continue
                print()
                msg    = new_msgs[0]
                msg_id = msg["id"]
                r2     = self.s.get(f"https://api.mail.tm/messages/{msg_id}", headers=auth, timeout=10)
                body   = r2.json().get("text", "") or r2.json().get("html", "") or ""
                match  = re.search(r"(\d{4,8})", body)
                if match:
                    otp = match.group(1)
                    self.seen_ids.add(msg_id)
                    log.info(f"MailTM OTP: {otp}")
                    print_ok(f"OTP diterima: {C.BOLD}{otp}{C.RESET}")
                    return otp
                else:
                    self.seen_ids.add(msg_id)
                    print_warn("Email masuk tapi tidak ada OTP — skip")
                    log.info("Email masuk tanpa OTP — skip")
            except Exception as e:
                log.warning(f"MailTM poll error: {e}")
        print()
        log.error(f"MailTM timeout {timeout}s")
        print_err(f"OTP tidak masuk dalam {timeout}s")
        return None

    def resend_otp_ready(self):
        if not self.token and not self.get_token(): return
        auth = {"Authorization": f"Bearer {self.token}"}
        try:
            r    = self.s.get("https://api.mail.tm/messages", headers=auth, timeout=10)
            msgs = r.json().get("hydra:member", [])
            for m in msgs:
                self.seen_ids.add(m["id"])
            log.info(f"MailTM snapshot: {len(self.seen_ids)} email lama ditandai")
            print_info(f"{len(self.seen_ids)} email lama ditandai — siap terima OTP baru")
        except Exception as e:
            log.warning(f"MailTM resend_otp_ready error: {e}")

# ============================================================
# CREATE WALLET
# ============================================================

def create_wallet():
    section("Create Wallet")

    # Buat email
    print_run("Membuat email temporer...")
    mail = MailTM()
    if not mail.create_account():
        print_err("Gagal buat email — abort")
        log.error("Gagal buat email"); return False
    print_ok(f"Email: {C.BOLD}{mail.address}{C.RESET}")

    # Navigasi + input email + send OTP
    print_run("Navigasi → form email → kirim OTP...")
    escaped_email = mail.address.replace(" ", "%s")
    cmd = (
        f"input tap {WALLET_TAB[0]} {WALLET_TAB[1]} && sleep {D['after_tap_wallet_tab']} && "
        f"input tap {CREATE_WALLET_BTN[0]} {CREATE_WALLET_BTN[1]} && sleep {D['after_create_wallet_btn']} && "
        f"input tap {AGREE_TERMS_BTN[0]} {AGREE_TERMS_BTN[1]} && sleep {D['after_agree_terms_btn']} && "
        f"input tap {EMAIL_FIELD[0]} {EMAIL_FIELD[1]} && sleep {D['after_tap_email_field']} && "
        f"input text {escaped_email} && sleep {D['after_type_email']} && "
        f"input tap {SEND_OTP_BTN[0]} {SEND_OTP_BTN[1]}"
    )
    vcadb_exec(cmd, poll_timeout=90)
    time.sleep(D["after_send_otp"])

    # Captcha manual
    print()
    print(f"  {C.YELLOW}⚠{C.RESET}   Buka VSPhone, verifikasi {C.BOLD}CAPTCHA{C.RESET} di device,")
    print(f"       lalu tekan {C.BOLD}ENTER{C.RESET} untuk lanjut.")
    print()
    input(f"  {C.BOLD}  → Tekan ENTER setelah captcha selesai...{C.RESET}  ")
    print()

    # Keep form aktif
    print_run("Menjaga form aktif (tap OTP field)...")
    vcadb_exec(f"input tap {OTP_FIELD[0]} {OTP_FIELD[1]}", poll_timeout=15)
    time.sleep(1)

    # Polling OTP — dengan retry
    otp = None
    while not otp:
        otp = mail.wait_for_otp(timeout=OTP_TIMEOUT, keepalive_tap=OTP_FIELD)
        if not otp:
            print_err("OTP tidak masuk")
            ans = input(f"\n  {C.BOLD}Kirim ulang OTP? (y = kirim ulang / n = skip):{C.RESET} ").strip().lower()
            if ans != "y":
                print_err("Skip device ini")
                log.error("User skip — OTP tidak masuk"); return False
            mail.resend_otp_ready()
            print_run("Kirim ulang OTP...")
            log.info("Kirim ulang OTP")
            vcadb_exec(f"input tap {SEND_OTP_BTN[0]} {SEND_OTP_BTN[1]}", poll_timeout=15)
            time.sleep(D["after_send_otp"])
            print()
            print(f"  {C.YELLOW}⚠{C.RESET}   Selesaikan CAPTCHA lagi jika muncul!")
            input(f"  {C.BOLD}  → Tekan ENTER setelah captcha selesai...{C.RESET}  ")
            print()

    # Input OTP + referral + next
    print_run(f"Input OTP + referral + next...")
    log.info(f"Input OTP={otp} referral={REFERRAL_CODE}")
    cmd = (
        f"input tap {OTP_FIELD[0]} {OTP_FIELD[1]} && sleep {D['after_tap_otp_field']} && "
        f"input text {otp} && sleep {D['after_type_otp']} && "
        f"input tap {REFF_DROPDOWN[0]} {REFF_DROPDOWN[1]} && sleep {D['after_tap_reff_dropdown']} && "
        f"input tap {REFF_FIELD[0]} {REFF_FIELD[1]} && sleep {D['after_tap_reff_field']} && "
        f"input text {REFERRAL_CODE} && sleep {D['after_type_reff']} && "
        f"input tap {NEXT_BUTTON_KB[0]} {NEXT_BUTTON_KB[1]}"
    )
    vcadb_exec(cmd, poll_timeout=60)
    time.sleep(D["after_next_button"])

    # Set password
    print_run("Set password...")
    ep = escape_adb(WALLET_PASSWORD)
    cmd1 = (
        f"input tap {PASS_FIELD[0]} {PASS_FIELD[1]} && sleep {D['after_tap_pass_field']} && "
        f"input text {ep} && sleep {D['after_type_password']}"
    )
    vcadb_exec(cmd1, poll_timeout=30)
    time.sleep(D["after_tap_confirm_pass"])

    cmd2 = (
        f"input tap {CONFIRM_PASS_KB[0]} {CONFIRM_PASS_KB[1]} && sleep {D['after_tap_confirm_pass']} && "
        f"input text {ep} && sleep {D['after_type_password']} && "
        f"input keyevent 4 && sleep {D['after_hide_keyboard']} && "
        f"input tap {AGREE_FORGET_CB[0]} {AGREE_FORGET_CB[1]} && sleep {D['after_agree_forget_cb']} && "
        f"input tap {FINAL_CONTINUE[0]} {FINAL_CONTINUE[1]}"
    )
    vcadb_exec(cmd2, poll_timeout=60)
    time.sleep(D["after_final_continue"])

    # Handle popup biometric
    print_run("Handle popup biometric...")
    cmd3 = (
        f"input tap {GOOGLE_SAVE_CANCEL[0]} {GOOGLE_SAVE_CANCEL[1]} && sleep {D['after_google_save_cancel']} && "
        f"input tap {SKIP_BIOMETRIC[0]} {SKIP_BIOMETRIC[1]} && sleep {D['after_skip_biometric']} && "
        f"input tap {SET_UP_LATER[0]} {SET_UP_LATER[1]}"
    )
    vcadb_exec(cmd3, poll_timeout=30)
    time.sleep(D["after_set_up_later"])

    # Simpan hasil
    result_line = f"Device={DEVICE_NAME} | Email={mail.address} | Pass={WALLET_PASSWORD} | Ref={REFERRAL_CODE}"
    log.info(f"WALLET OK: {result_line}")
    with open("wallet_sukses.txt", "a", encoding="utf-8") as f:
        f.write(result_line + "\n")

    print()
    box_top("Wallet Berhasil Dibuat!", C.GREEN)
    box_mid(f"Device  : {DEVICE_NAME}", C.GREEN, C.WHITE)
    box_mid(f"Email   : {mail.address}", C.GREEN, C.WHITE)
    box_mid(f"Pass    : {WALLET_PASSWORD}", C.GREEN, C.WHITE)
    box_mid(f"Ref     : {REFERRAL_CODE}", C.GREEN, C.WHITE)
    box_mid(f"Tersimpan di wallet_sukses.txt", C.GREEN, C.DIM)
    box_bot(C.GREEN)

    return mail

# ============================================================
# FACTORY RESET
# ============================================================

def factory_reset():
    section("Factory Reset")
    try:
        r = session.post(
            f"{BASE}/padManage/padReset",
            json={"padCodes": [PAD_CODE]},
            headers=headers, timeout=15
        )
        d = r.json()
        if d.get("code") == 200:
            log.info("Factory reset command dikirim via API")
            print_ok("Factory reset command dikirim via API")
        else:
            log.warning(f"API reset gagal: {d} — fallback ADB")
            print_warn("API reset gagal — fallback ke ADB")
            vcadb_exec(
                "am broadcast -a android.intent.action.MASTER_CLEAR -n android/com.android.server.MasterClearReceiver",
                poll_timeout=30
            )
    except Exception as e:
        log.warning(f"API reset exception: {e} — fallback ADB")
        print_warn(f"Exception — fallback ke ADB")
        vcadb_exec(
            "am broadcast -a android.intent.action.MASTER_CLEAR -n android/com.android.server.MasterClearReceiver",
            poll_timeout=30
        )
    countdown(FACTORY_RESET_WAIT, "Tunggu device reset selesai")
    print_ok("Factory reset selesai")
    log.info("Factory reset selesai")

# ============================================================
# GET SEED PHRASE
# ============================================================

def get_seed_phrase(mail: MailTM) -> str | None:
    section("Get Seed Phrase")

    # Snapshot inbox sebelum OTP dikirim
    print_run("Snapshot inbox sebelum OTP dikirim...")
    mail.resend_otp_ready()

    # Wallet → Settings → Recovery Phrase → Confirm Risk Warning
    print_run("Navigasi ke Show Recovery Phrase...")
    log.info("Navigasi ke recovery phrase")
    cmd = (
        f"input tap {WALLET_TAB[0]} {WALLET_TAB[1]} && sleep {D['after_tap_wallet_tab']} && "
        f"input tap {SETTINGS_BTN[0]} {SETTINGS_BTN[1]} && sleep 4 && "
        f"input tap {SHOW_RECOVERY_PHRASE[0]} {SHOW_RECOVERY_PHRASE[1]} && sleep 4 && "
        f"input tap {RISK_WARNING_CONFIRM[0]} {RISK_WARNING_CONFIRM[1]}"
    )
    vcadb_exec(cmd, poll_timeout=40)
    time.sleep(5)

    # Poll OTP
    otp = None
    while not otp:
        otp = mail.wait_for_otp(timeout=OTP_TIMEOUT)
        if not otp:
            print_err("OTP seed phrase tidak masuk")
            ans = input(f"\n  {C.BOLD}Retry? (y/n):{C.RESET} ").strip().lower()
            if ans != "y":
                print_err("Skip seed phrase")
                log.error("Skip seed phrase — user abort"); return None
            mail.resend_otp_ready()

    # Input OTP → Confirm
    print_run(f"Input OTP seed phrase...")
    log.info(f"Input OTP seed phrase: {otp}")
    cmd = (
        f"input tap {SEED_OTP_FIELD[0]} {SEED_OTP_FIELD[1]} && sleep 2 && "
        f"input text {otp} && sleep 2 && "
        f"input tap {SEED_OTP_CONFIRM[0]} {SEED_OTP_CONFIRM[1]}"
    )
    vcadb_exec(cmd, poll_timeout=30)
    print_ok("OTP seed phrase berhasil diinput")
    log.info("OTP seed phrase diinput OK")
    return True

# ============================================================
# MAIN
# ============================================================

def main():
    banner()

    login()
    time.sleep(1)

    # Input referral
    global REFERRAL_CODE
    print()
    print(f"  {C.CYAN}Referral code saat ini:{C.RESET} {C.BOLD}{REFERRAL_CODE}{C.RESET}")
    ref_input = input("  Masukkan referral baru (kosong = pakai default): ").strip()
    if ref_input:
        REFERRAL_CODE = ref_input
        print_ok(f"Referral diset → {C.BOLD}{REFERRAL_CODE}{C.RESET}")
        log.info(f"Referral: {REFERRAL_CODE}")
    else:
        print_info(f"Pakai default: {C.BOLD}{REFERRAL_CODE}{C.RESET}")
        log.info(f"Referral default: {REFERRAL_CODE}")

    # Pilih APK
    apk_result = get_topnod_apk()
    if apk_result is None:
        print_err("APK TopNod tidak ditemukan — abort")
        log.error("APK tidak ditemukan"); return
    if isinstance(apk_result, list):
        while True:
            try:
                c = int(input(f"\n  Pilih nomor APK (1-{len(apk_result)}): "))
                if 1 <= c <= len(apk_result): break
            except ValueError: pass
        apk_info = apk_result[c - 1]
    else:
        apk_info = apk_result

    # Summary konfigurasi
    print()
    box_top("Konfigurasi", C.BLUE)
    box_mid(f"Device   : {DEVICE_NAME}", C.BLUE, C.WHITE)
    box_mid(f"APK      : {apk_info['fileName']}", C.BLUE, C.WHITE)
    box_mid(f"Referral : {REFERRAL_CODE}", C.BLUE, C.WHITE)
    box_mid(f"Log file : {log_filename}", C.BLUE, C.DIM)
    box_bot(C.BLUE)
    print()

    try:
        # Install
        install_apk(apk_info)

        # Launch
        if not launch_app():
            print_err("Launch gagal — abort")
            log.error("Launch gagal"); return

        # Set resolusi
        set_resolution()
        time.sleep(3)

        # Create wallet
        mail = create_wallet()
        if mail:
            countdown(10, "Tunggu app stabil")
            get_seed_phrase(mail)

        print()
        print_ok("Selesai.")
        log.info("Script selesai")

    except KeyboardInterrupt:
        print()
        box_top("Script Dihentikan", C.YELLOW)
        box_mid("Script dihentikan manual (Ctrl+C)", C.YELLOW, C.WHITE)
        box_bot(C.YELLOW)
        log.info("Script dihentikan manual")
    except Exception as e:
        print()
        print_err(f"Error fatal: {e}")
        log.error(f"Error fatal: {e}")


if __name__ == "__main__":
    main()

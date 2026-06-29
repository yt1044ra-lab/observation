from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

USERS = {
    1:"池田", 2:"石川", 3:"今西", 4:"遠藤", 5:"大杉",
    6:"大竹", 7:"大橋", 8:"緒方", 9:"小笹", 10:"桂",
    11:"小寺", 12:"近藤", 13:"佐藤", 14:"澤田", 15:"繁田",
    16:"島崎", 17:"進藤", 18:"新保", 19:"鈴木", 20:"髙瀬",
    21:"棚瀬", 22:"冨永", 23:"永井", 24:"平間", 25:"廣瀬",
    26:"前田", 27:"松田", 28:"万浪", 29:"萬谷", 30:"三宅",
    31:"村上", 32:"森永", 33:"守屋", 34:"矢崎", 35:"山田",
    36:"吉田", 37:"若子", 38:"髙梨"
}

ADMIN_PASSWORD = "1234"

GLOBAL_MESSAGE = ""

MESSAGE_HISTORY = []

INCIDENT_HISTORY = []

AREA_STATUS = {
    "mission1": {"status": "正常", "person": "-"},
    "mission2": {"status": "正常", "person": "-"},
    "mission3": {"status": "正常", "person": "-"},
    "mission4": {"status": "正常", "person": "-"},
    "mission5": {"status": "正常", "person": "-"},
    "exit": {"status": "正常", "person": "-"}
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login/<area>")
def login(area):
    return render_template("login.html", area=area)


@app.route("/authenticate/<area>", methods=["POST"])
def authenticate(area):

    try:
        number = int(request.form["number"])
    except:
        return "番号を入力してください"

    if number not in USERS:
        return "存在しない番号です"

    AREA_STATUS[area]["person"] = USERS[number]

    return redirect(f"/operator/{area}/{number}")


@app.route("/operator/<area>/<int:number>")
def operator(area, number):

    return render_template(
        "operator.html",
        area=area,
        number=number,
        name=USERS[number],
        status=AREA_STATUS[area]["status"],
        message=GLOBAL_MESSAGE
    )


@app.route("/report_crowd/<area>/<int:number>")
def report_crowd(area, number):

    AREA_STATUS[area]["status"] = "混雑"
    AREA_STATUS[area]["person"] = USERS[number]

    INCIDENT_HISTORY.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "area": area,
            "person": USERS[number],
            "status": "混雑"
        }
    )

    return redirect(f"/operator/{area}/{number}")


@app.route("/report_failure/<area>/<int:number>")
def report_failure(area, number):

    AREA_STATUS[area]["status"] = "故障"
    AREA_STATUS[area]["person"] = USERS[number]

    INCIDENT_HISTORY.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "area": area,
            "person": USERS[number],
            "status": "故障"
        }
    )

    return redirect(f"/operator/{area}/{number}")


@app.route("/other_form/<area>/<int:number>")
def other_form(area, number):

    return render_template(
        "other_report.html",
        area=area,
        number=number,
        name=USERS[number]
    )


@app.route("/send_other/<area>/<int:number>", methods=["POST"])
def send_other(area, number):

    detail = request.form["detail"]

    AREA_STATUS[area]["status"] = "その他"
    AREA_STATUS[area]["person"] = USERS[number]

    INCIDENT_HISTORY.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "area": area,
            "person": USERS[number],
            "status": f"その他：{detail}"
        }
    )

    return redirect(f"/operator/{area}/{number}")


@app.route("/resolve/<area>/<int:number>")
def resolve(area, number):

    AREA_STATUS[area]["status"] = "正常"

    INCIDENT_HISTORY.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "area": area,
            "person": USERS[number],
            "status": "問題解決"
        }
    )

    return redirect(f"/operator/{area}/{number}")


@app.route("/logout/<area>")
def logout(area):

    AREA_STATUS[area]["person"] = "-"
    AREA_STATUS[area]["status"] = "正常"

    return redirect("/")


@app.route("/admin")
def admin():
    return render_template("admin_login.html")


@app.route("/admin_auth", methods=["POST"])
def admin_auth():

    try:
        number = int(request.form["number"])
    except:
        return "番号を入力してください"

    password = request.form["password"]

    if number not in [20, 21]:
        return "管理者権限がありません"

    if password != ADMIN_PASSWORD:
        return "パスワードが違います"

    return redirect("/admin_view")


@app.route("/send_message", methods=["POST"])
def send_message():

    global GLOBAL_MESSAGE

    message = request.form["message"]

    GLOBAL_MESSAGE = message

    MESSAGE_HISTORY.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": message
        }
    )

    return redirect("/admin_view")


@app.route("/admin_view")
def admin_view():

    return render_template(
        "admin.html",
        areas=AREA_STATUS,
        message=GLOBAL_MESSAGE,
        messages=MESSAGE_HISTORY,
        incidents=INCIDENT_HISTORY
    )


if __name__ == "__main__":
    app.run(debug=True)
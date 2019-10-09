// 閉じるフラグ
var flag = true;

// サーバーを起動
function start_server() {
    $("#server_btn").on("click", function () {
        $.ajax({
            url: "server.php",
            type: "POST",
            data: {
                "func": "start_server"
            }
        })
            .done(function (data) {
                console.log("サーバーを起動しました");
                console.log(data);
            })
            .fail(function () {
                console.log("失敗しました");
            });
    });
}

// プレイヤーをログアウトさせる
function del_player() {
    $(window).on("beforeunload", function () {
        if (flag) {
            var urlParams = new URLSearchParams(window.location.search);
            var result = $.isEmptyObject(urlParams);
            if (!result) {
                var player_name = urlParams.get("player_name");
                $.ajax({
                    url: "cgi-bin/ajax.py",
                    type: "POST",
                    async: false,
                    data: {
                        "func": "del_player",
                        "player_name": player_name
                    }
                })
            }
        }
    });
}

// 作成済みのルームを選択リストに追加する
function append_room() {
    $.ajax({
        url: "cgi-bin/ajax.py",
        type: "POST",
        dataType: "json",
        async: false,
        data: {
            "func": "get_room_name"
        }
    })
        .done(function (data) {
            console.log("ルームリストを更新しました。")
            if (!Object.keys(data).length) {
                console.log("現在ルームはありません。");
            }
            else {
                console.log(data);
            }
            for (room_name in data) {
                if (data[room_name] >= 5) {
                    console.log(room_name + "は満員です。");
                    $("#room_list").append("<option disabled>" + room_name + "</option>");
                }
                else {
                    $("#room_list").append("<option>" + room_name + "</option>");
                    $(".join_room").append("<div class='content'><h3 class='room_name'>" + room_name + "</h3>" + "<h3 class='player_num'>" + "現在：" + data[room_name] + "人</h3>" + "<button class='enter_room_btn'>参加</button></div>");
                }

            }
        })
        .fail(function (data) {
            console.log("fail");
        })
}

// ルームを選択する
function select_room() {
    $(document).on("click", ".enter_room_btn", function () {
        console.log("ok");
        var urlParams = new URLSearchParams(window.location.search);
        var room_name = $(this).parent().find(".room_name").text();
        console.log("クリックされました");
        console.log($(this));
        console.log(room_name);
        var player_name = urlParams.get("player_name");
        var url = "htmls/room.html?room_name=" + room_name + "&player_name=" + player_name;
        flag = false;
        window.location.href = url;
    });
}

// ルームを生成する
function create_room() {
    $("#create_room").on("click", function (e) {
        e.preventDefault();
        var room_name = $("[name='room_name']").val();
        $("[name='room_name']").val("");
        console.log(room_name);
        $.ajax({
            url: "cgi-bin/ajax.py",
            type: "POST",
            async: false,
            dataType: "json",
            data: {
                "func": "create_room",
                "room_name": room_name
            }
        })
            .done(function (data) {
                console.log("success");
                console.log(data);
                var urlParams = new URLSearchParams(window.location.search);
                var player_name = urlParams.get("player_name");
                var url = "htmls/room.html?room_name=" + room_name + "&player_name=" + player_name;
                flag = false;
                window.location.href = url;
            })
            .fail(function (data) {
                console.log("fails");
                console.log(data);
            });
    });
}

// プレイヤーを生成する
function create_player() {
    $("#create_player").on("click", function (e) {
        e.preventDefault();
        var player_name = $("[name='player_name']").val();
        $("[name='player_name']").val("");
        $.ajax({
            url: "cgi-bin/ajax.py",
            type: "POST",
            dataType: "json",
            // async: false,
            data: {
                "func": "create_player",
                "player_name": player_name
            }
        })
            .done(function (data) {
                console.log("success");
                console.log(data);
                var url = "?player_name=" + data["player_name"];
                var path = location.pathname;
                window.history.pushState(null, null, path + url);
                set_player_name();
                show_contents();
                hide_create_player();
            })
            .fail(function () {
                console.log("プレイヤーの登録に失敗しました");
            });
    });
}

// プレイヤー名をセットする
function set_player_name() {
    var urlParams = new URLSearchParams(window.location.search);
    var result = $.isEmptyObject(urlParams);
    if (!result) {
        var player_name = urlParams.get("player_name");
        $("#player_name").html(player_name);
    }
}


function show_create_room() {
    $("#create_room_link").on("click", function (e) {
        e.preventDefault();
        $(".create_room").show();
        hide_join_room();
    });
}

function show_join_room() {
    $("#join_room_link").on("click", function (e) {
        e.preventDefault();
        $(".join_room").show();
        // $("content").show();
        hide_create_room();
    });
}

function hide_create_room() {
    $(".create_room").hide();
}

function hide_join_room() {
    $(".join_room").hide();
}

function show_contents() {
    $(".contents").show();
}

function hide_contents() {
    $(".contents").hide();
    hide_create_room();
    hide_join_room();
}

function hide_create_player() {
    $(".create_player").hide();
}

function show_create_player() {
    $(".create_player").show();
}

// ページ読み込み時の動作
window.onload = function () {
    var urlParams = new URLSearchParams(window.location.search);

    // プレイヤーを登録していなかったら
    if (urlParams.get(["player_name"]) == null) {
        this.show_create_player();
        hide_contents();
        append_room();
        console.log("プレイヤー名を入力してください。");
    }
    else {
        this.append_room();
        hide_create_player();
        this.hide_join_room();
        this.hide_create_room();
    }
}

$(function () {
    start_server();
    set_player_name();
    create_player();
    show_create_room();
    show_join_room();
    create_room();
    select_room();
    del_player();
});
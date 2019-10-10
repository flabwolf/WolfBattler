// 作成済みのルームを選択リストに追加する
function append_room() {
    $.ajax({
        url: "../cgi-bin/ajax.py",
        type: "POST",
        dataType: "json",
        async: false,
        data: {
            "func": "get_room_name"
        }
    })
        .done(function (data) {
            console.log("ルームリストを更新しました。");
            $(".room_list").text("");
            if (!Object.keys(data).length) {
                console.log("現在ルームはありません。");
                $(".room_list").append("<div class='content'><h3 class='room_name'>" + "現在作成されてるルームはありません" + "</h3></div>")
            }
            else {
                console.log(data);
            }
            for (room_name in data) {
                if (data[room_name] >= 5) {
                    console.log(room_name + "は満員です。");
                }
                else {
                    $(".room_list").append("<div class='content'><h3 class='room_name'>" + room_name + "</h3>" + "<button class='delete_room_btn'>削除</button></div>");
                }

            }
        })
        .fail(function (data) {
            console.log("fail");
        });
}

// 作成済みのプレイヤーをリストに追加する
function append_player() {
    $.ajax({
        url: "../cgi-bin/ajax.py",
        type: "POST",
        dataType: "json",
        async: false,
        data: {
            "func": "get_player_name"
        }
    })
        .done(function (data) {
            console.log("プレイヤーリストを更新しました。");
            $(".player_list").text("");
            if (!Object.keys(data).length) {
                console.log("現在プレイヤーはいません");
                $(".player_list").append("<div class='content'><h3 class='player_name'>" + "現在プレイヤーはいません" + "</h3></div>")
            }
            else {
                console.log(data);
            }
            for (player_name in data) {
                $(".player_list").append("<div class='content'><h3 class='player_name'>" + player_name + "</h3>" + "<button class='delete_player_btn'>削除</button></div>");
            }
        })
        .fail(function (data) {
            console.log("fail");
        });
}

// ルームを削除する
function delete_room() {
    $(document).on("click", ".delete_room_btn", function () {
        var room_name = $(this).parent().find(".room_name").text();
        console.log($(this));
        console.log(room_name);
        $.ajax({
            url: "../cgi-bin/ajax.py",
            type: "POST",
            data: {
                "func": "admin_del_room",
                "room_name": room_name
            }
        })
            .done(function (data) {
                console.log(room_name + "を削除しました");
                append_room();
            })
            .fail(function () {
                console.log("削除に失敗しました");
            });
    });
}

// プレイヤーを削除する
function delete_player() {
    $(document).on("click", ".delete_player_btn", function () {
        var player_name = $(this).parent().find(".player_name").text();
        console.log($(this));
        console.log(player_name);
        $.ajax({
            url: "../cgi-bin/ajax.py",
            type: "POST",
            data: {
                "func": "admin_del_player",
                "player_name": player_name
            }
        })
            .done(function (data) {
                console.log(player_name + "を削除しました");
                append_player();
            })
            .fail(function () {
                console.log("削除に失敗しました");
            });
    });
}

function show_player_list() {
    $("#player_link").on("click", function (e) {
        e.preventDefault();
        $(".player_list").show();
        hide_room_list();
    });
}

function show_room_list() {
    $("#room_link").on("click", function (e) {
        e.preventDefault();
        append_room();
        $(".room_list").show();
        // $("content").show();
        hide_player_list();
    });
}

function show_player_list() {
    $("#player_link").on("click", function (e) {
        e.preventDefault();
        append_player();
        $(".player_list").show();
        // $("content").show();
        hide_room_list();
    });
}

function hide_player_list() {
    $(".player_list").hide();
}

function hide_room_list() {
    $(".room_list").hide();
}

window.onload = function () {
    this.append_player();
    this.hide_room_list();
    this.hide_player_list();
}

$(function () {
    show_player_list();
    show_room_list();
    delete_room();
    delete_player();
})
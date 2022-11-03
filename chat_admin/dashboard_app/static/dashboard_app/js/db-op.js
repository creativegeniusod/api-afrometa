
const headers = {
    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
};

const APICall = (data) => {
    let _self = $(this);
    console.log('headers', headers);
    $.ajax({
        url: '/dashboard/dbops/purge/',
        type: 'POST',
        headers: headers,
        data: data,
        success: function(res) {
            $.notify('Data Purged.', 'success', { position:"right" });
        },
        error: function(err) {
            $.notify(err.exception ? err.exception : 'Something went Wrong.', 'error', { position:"right" });
        }
    });
};

const purgeChatRooms = () => {
    if ( confirm(`All chat history of the rooms will also be deleted. Are you sure to proceed?`) ) {
        APICall({ "op": "cr" });
    }
};

const purgeRoomsChatHistory = () => {
    if ( confirm(`Are you sure to proceed?`) ) {
        APICall({ "op": "rch" });
    }
};

const purgeAllMessageHistory = () => {
    if ( confirm(`Are you sure to proceed?`) ) {
        APICall({ "op": "amh" });
    }
};


$(document).ready(function() {

    $(document).on('click', '.purge-op', function(event) {
        switch($(this).data("op")) {
            case "cr":
                purgeChatRooms();
                break;
            case "rch":
                purgeRoomsChatHistory();
                break;
            case "amh":
                purgeAllMessageHistory();
                break;
        }
    });
});

$(document).ready(function() {

    displayLeaderboard = function(top_ideas)
    {
        console.log(top_ideas);
        leaders = "";
        for (var i in top_ideas)
        {
            var idea = top_ideas[i];
            leaders += "<div class='idea' <span class='votes "
                        + idea._id + "'>" + idea.votes + "</span> "
                        + idea.company + " for " + idea.industry 
                        + "</br> </div>";
        }
        $(".leaderboard-itemholder").html(leaders);
    }

    $(".upvote").click( function() {
        id = $(this).attr('objectid');
        data = new Object();
        data.company = $('.company').html();
        console.log("data company" + data.company);
        data.industry = $('.industry').html();
        data.votes = $('.votes.' + id).html();
        $.ajax({
            type: 'POST',
            url: "/upvote",
            data: data,
            success: function(data) {
                $(".votes."+id).html(data.votes);
                var top_ideas = data.top_ideas;
                displayLeaderboard(top_ideas);
            }
        });
    });

    $("#newidea-button").click( function() {
        $.ajax({
            type: 'POST',
            url: "/new_idea",
            success: function(data) {
                old_id = $(".upvote").attr("objectid");
                $(".upvote").attr("objectid", data._id);
                node = $("#idea-lineholder .votes."+old_id);
                $("#idea-lineholder .votes."+old_id).html(data.votes);
                $("#idea-lineholder .votes."+old_id).attr("class", "votes "+data._id);
                $(".company").html(data.company);
                $(".industry").html(data.industry);
                var top_ideas = data.top_ideas;
                displayLeaderboard(top_ideas);

            }
        });
    });

    $("#add-company .add-button").click( function() 
    {
        data = new Object();
        data.company = $("#add-company-text").val().toString();
        if (data.company == "")
            return;
        if (data.company === "add company")
        {
            node = $("#add-company .confirm-container .confirm");
            node.show();
            msg = "invalid company";
            node.css("color", "red");
            node.html(msg);
            node.fadeOut(2000);
            return;
        }
        $.ajax(
        {
            type: "POST", 
            url: "/add_company",
            data: data, 
            success: function(data) 
            {   
                node = $("#add-company .confirm-container .confirm");
                node.show();
                msg = data.message;
                if (msg.indexOf("already") !== -1)
                {
                    node.css("color", "red");
                }
                else 
                {
                    node.css("color", "lime");
                }
                node.html(msg);
                node.fadeOut(2000);
            }
        });
    });

    $("#add-industry .add-button").click( function() 
    {
        data = new Object();
        data.industry = $("#add-industry-text").val().toString();
        if (data.industry == "")
            return;
        if (data.industry === "add industry")
        {
            node = $("#add-industry .confirm-container .confirm");
            node.show();
            msg = "invalid industry";
            node.css("color", "red");
            node.html(msg);
            node.fadeOut(2000);
            return;
        }
        $.ajax(
        {
            type: "POST",
            url: "/add_industry",
            data: data,
            success: function(data) 
            {
                node = $("#add-industry .confirm-container .confirm");
                node.show();
                msg = data.message;
                if (msg.indexOf("already") !== -1)
                {
                    node.css("color", "red");
                }
                else 
                {
                    node.css("color", "lime");
                } 
                console.log(msg);
                node.html(msg);
                node.fadeOut(2000);
            }
        });
    }); 

    $(".add-button").click( function()
    {
        textbox_node = $(this).prev();
        textbox_node.select();
    });

    $(".textbox").click( function() {
       id = $(this).attr("id"); 
       $("#"+id).val("");
       $("#"+id).select();
    });

    $(".textbox").keypress( function (e)
    {
        code = (e.keyCode ? e.keyCode : e.which);
        if (code == 13) 
        {
            $(this).next().click();
        }
    });
});

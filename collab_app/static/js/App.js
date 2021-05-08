
$(document).ready(() => {

  $('#sf').submit((e) => {
      e.preventDefault();
      input = $('#search_bar').val();
      location.href = '/' + input

    
  })

  $('#search_trgt').on('click', () => {
      input = $('#search_bar').val();
      location.href = '/' + input
  })

  $('#search_trgt').on('keydown', (e) => {
    alert("wa")
    if (e.keyCode == 13) {
      e.preventDefault();
      console.log("one")
      input = $('#search_bar').val();
      location.href = '/' + input
    }
})



  $('#RDJ').on('click', () => {

    const options = {
      method: 'GET',
      url: 'https://dad-jokes.p.rapidapi.com/random/joke',
      headers: {
        'x-rapidapi-key': '798288d5aemsh909a16f4fd3e801p1d0d40jsn59e95721a92f',
        'x-rapidapi-host': 'dad-jokes.p.rapidapi.com'
      }
    };
    
    axios.request(options).then(function (response) {
      console.log(response.data.body[0].setup)
      $('#RDJ_setup').text(response.data.body[0].setup)
      $('#RDJ_punchline').text(response.data.body[0].punchline)
      $('#RDJ_modal').show()
    }).catch(function (error) {
      console.error(error);
    });

    const offset = Math.random() * 20;
  

    const gif = {
      method: 'GET',
      url: 'https://api.giphy.com/v1/gifs/search?api_key=sTBjdQRhYRoYXHDzETUULI05YxSU1clP',
      params: {
        'q': 'laughing',
        'limit': 1,
        'rating': 'pg',
        'lang': 'en',
        'offset': Math.floor(offset),
      }

    };
    
    axios.request(gif).then(function (response) {
      data = response.data.data[0].images.downsized.url;
      $('#RDJ_GIF').html('<center><img src = "'+data+'"  title="GIF via Giphy"></center>')
      $('#RDJ_modal').show()
    }).catch(function (error) {
      console.error(error);
    });

    $('#RDJ_close').on('click', () => {
        $("#RDJ_modal").hide()
    })
  })

  //---------------------
  $('#RIQ').on('click', () => {

    const quote = {
      method: 'GET',
      url: 'https://geek-jokes.sameerkumar.website/api?format=json',
    };
    
    axios.request(quote).then(function (response) {
      console.error(response);
      $('#RIQ_quote').text(response.data.joke)
    }).catch(function (error) {
      console.error(error);
    });

    const offset = Math.random() * 20;
  

    const gif = {
      method: 'GET',
      url: 'https://api.giphy.com/v1/gifs/search?api_key=sTBjdQRhYRoYXHDzETUULI05YxSU1clP',
      params: {
        'q': 'chuck norris',
        'limit': 1,
        'rating': 'pg',
        'lang': 'en',
        'offset': Math.floor(offset),
      }
    };


    
    
    axios.request(gif).then(function (response) {
      data = response.data.data[0].images.downsized.url;
      $('#RIQ_GIF').html('<center><img src = "'+data+'"  title="GIF via Giphy"></center>')
      $('#RIQ_modal').show()
    }).catch(function (error) {
      console.error(error);
    });

  
    $('#RIQ_close').on('click', () => {
        $("#RIQ_modal").hide()
    })
  })

  $('#ROQ').on('click', () => {

    const quote = {
      method: 'GET',
      url: 'https://officeapi.dev/api/quotes/random',
    };
    
    axios.request(quote).then(function (response) {
      console.log(response)
      $('#ROQ_quote').text(response.data.data.content)
    }).catch(function (error) {
      console.error(error);
    });

    const offset = Math.random() * 20;
  

    const gif = {
      method: 'GET',
      url: 'https://api.giphy.com/v1/gifs/search?api_key=sTBjdQRhYRoYXHDzETUULI05YxSU1clP',
      params: {
        'q': 'the office',
        'limit': 1,
        'rating': 'pg',
        'lang': 'en',
        'offset': Math.floor(offset),
      }
    };

    
    
    axios.request(gif).then(function (response) {
      data = response.data.data[0].images.downsized.url;
      $('#ROQ_GIF').html('<center><img src = "'+data+'"  title="GIF via Giphy"></center>')
      $('#ROQ_modal').show()
    }).catch(function (error) {
      console.error(error);
    });

  
    $('#ROQ_close').on('click', () => {
        $("#ROQ_modal").hide()
    })
  })


  $('#search_bar').on("keyup", async () => {
    console.log($('#search_bar').val())
    if ($('#search_bar').val() != "") {
      const word = $('#search_bar').val();
      $.ajax({ 
        url: "/get_classes/"+word
      }).then(function(res) { 
        while (document.getElementById("cs").firstChild) {
          document.getElementById("cs").removeChild(document.getElementById("cs").lastChild)
        }
        console.log(res)
        res.posts.forEach((x) => {
          console.log(x[0])
          let op = document.createElement("option")
          op.value = x[0];
          document.getElementById("cs").appendChild(op)
        })
      }); 
  

    
  
  
  }
})



})

const loadInfo = async (id) => {
  
  console.log("heres")
  $.ajax({ 
    url: "/getInfo/"+id 
  }).then(function(res) { 
    console.log(res)
    post = res.post
    $('#info_title').text(post[3])
    $('#info_start_time').text(post[9])
    $('#info_duration').text()
    $('#info_type').text(post[6])
    $('#info_location').text(post[8])
    $('#info_description').text(post[5])


    members = res.members
    members.forEach((member) => {
      let op = document.createElement("li")
        op.text = member[0] +  " "  + member[2];
        document.getElementById("info_members").appendChild(op)
    })

    $('#infoModal').modal('show')


  }); 

}


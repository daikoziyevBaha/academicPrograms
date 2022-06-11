
$("#id_passport_scan").change(function(){
	if (window.FormData === undefined) {
		alert('В вашем браузере FormData не поддерживается')
	} else {
		var formData = new FormData();
		formData.append('passport_scan', $("#id_passport_scan")[0].files[0]);
		formData.append('application_id', $("#id_application_id").val())

		fetch('applicaiton/',{
			headers: {
				'Content-Type':'application/json'
			},
			body:{name: 'hello'}, 
			method:"post"
		}).then(res => res.json()).then(data => {
			console.log(data.username)
		})

		$.ajax({
			type: "POST",
			url: "/application/application-details/documents-edit/add-document",
			cache: false,
			contentType: false,
			processData: false,
			data: formData,
			dataType : 'json',
			success: function(msg){
				if (msg.error == '') {
					$("#id_passport_scan").hide();
					$('#result').html(msg.success);
				} else {
					$('#result').html(msg.error);
				}
			}
		});
	}
});
$("#id_transcript_scan").change(function(){
	if (window.FormData === undefined) {
		alert('В вашем браузере FormData не поддерживается')
	} else {
		var formData = new FormData();
		formData.append('transcript_scan', $("#id_transcript_scan")[0].files[0]);
        formData.append('application_id', $("#id_application_id").val())
		$.ajax({
			type: "POST",
			url: "/application/application-details/documents-edit/add-document",
			cache: false,
			contentType: false,
			processData: false,
			data: formData,
			dataType : 'json',
			success: function(msg){
				if (msg.error == '') {
					$("#id_transcript_scan").hide();
					$('#result').html(msg.success);
				} else {
					$('#result').html(msg.error);
				}
			}
		});
	}
});
$("#id_motivation_scan").change(function(){
	if (window.FormData === undefined) {
		alert('В вашем браузере FormData не поддерживается')
	} else {
		var formData = new FormData();
		formData.append('motivation_scan', $("#id_motivation_scan")[0].files[0]);
        formData.append('application_id', $("#id_application_id").val())
 
		$.ajax({
			type: "POST",
			url: "/application/application-details/documents-edit/add-document",
			cache: false,
			contentType: false,
			processData: false,
			data: formData,
			dataType : 'json',
			success: function(msg){
				if (msg.error == '') {
					$("#id_motivation_scan").hide();
					$('#result').html(msg.success);
				} else {
					$('#result').html(msg.error);
				}
			}
		});
	}
});
$("#id_english_scan").change(function(){
	if (window.FormData === undefined) {
		alert('В вашем браузере FormData не поддерживается')
	} else {
		var formData = new FormData();
		formData.append('english_scan', $("#id_english_scan")[0].files[0]);
        formData.append('application_id', $("#id_application_id").val())

		$.ajax({
			type: "POST",
			url: "/application/application-details/documents-edit/add-document",
			cache: false,
			contentType: false,
			processData: false,
			data: formData,
			dataType : 'json',
			success: function(msg){
				if (msg.error == '') {
					$("#id_english_scan").hide();
					$('#result').html(msg.success);
				} else {
					$('#result').html(msg.error);
				}
			}
		});
	}
});
$("#id_recommendation_scan").change(function(){
	if (window.FormData === undefined) {
		alert('В вашем браузере FormData не поддерживается')
	} else {
		var formData = new FormData();
		formData.append('recommendation_scan', $("#id_recommendation_scan")[0].files[0]);
        formData.append('application_id', $("#id_application_id").val())

		$.ajax({
			type: "POST",
			url: "/application/application-details/documents-edit/add-document",
			cache: false,
			contentType: false,
			processData: false,
			data: formData,
			dataType : 'json',
			success: function(msg){
				if (msg.error == '') {
					$("#id_recommendation_scan").hide();
					$('#result').html(msg.success);
				} else {
					$('#result').html(msg.error);
				}
			}
		});
	}
});
$("#id_vaccination_scan").change(function(){
	if (window.FormData === undefined) {
		alert('В вашем браузере FormData не поддерживается')
	} else {
		var formData = new FormData();
		formData.append('vaccination_scan', $("#id_vaccination_scan")[0].files[0]);
        formData.append('application_id', $("#id_application_id").val())

		$.ajax({
			type: "POST",
			url: "/application/application-details/documents-edit/add-document",
			cache: false,
			contentType: false,
			processData: false,
			data: formData,
			dataType : 'json',
			success: function(msg){
				if (msg.error == '') {
					$("#id_vaccination_scan").hide();
					$('#result').html(msg.success);
				} else {
					$('#result').html(msg.error);
				}
			}
		});
	}
});

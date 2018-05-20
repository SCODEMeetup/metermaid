$(document).ready(function(){
	// When page loads...:
	$("div.content div").hide(); // Hide all content
	$("nav li:first").addClass("current").show(); // Activate first page
	$("div.content div:first").show(); // Show first page content

	// On Click Event (within list-element!)
	$("nav li").click(function() {
		$("nav li").removeClass("current"); // Remove any active class
		$(this).addClass("current"); // Add "current" class to selected page

		$("div.content div").hide(); // Hide all content

    // Find the href attribute value to identify the active page+content:
		var activePage = $(this).find("a").attr("href");
		$(activePage).fadeIn(); // Fade in the active page content
	}); // end click method

}); // end $(document).ready method

/**
 * Smart Link Router
 * 
 * Intercepts clicks on Travelpayouts affiliate links that are currently 
 * returning "marker is not subscribed" errors and automatically redirects 
 * the user to the intended clean, non-affiliate destination.
 * 
 * This allows the site to keep the affiliate structure in the markdown 
 * so that when the site gains traffic and gets approved, this script 
 * can simply be removed.
 */

(function () {
    document.addEventListener('click', function (e) {
        // Find the closest anchor tag that was clicked
        const link = e.target.closest('a');

        // If not a link, or not an affiliate link, do normal behavior
        if (!link || !link.href || !link.href.includes('tp.media/r')) return;

        // Specific P_IDs that are currently unapproved
        const unapprovedPartners = [
            'p=121', // Booking.com
            'p=125', // TripAdvisor
            'p=285', // Hotels.com
            'p=170'  // Lonely Planet
        ];

        const isUnapproved = unapprovedPartners.some(p => link.href.includes(p));

        if (isUnapproved) {
            // Prevent the default Travelpayouts broken redirect
            e.preventDefault();
            e.stopPropagation(); // Guarantee we intercept it

            // Extract the original destination URL from the 'u=' parameter
            try {
                const urlObj = new URL(link.href);
                const encodedDest = urlObj.searchParams.get('u');
                if (encodedDest) {
                    const cleanUrl = decodeURIComponent(encodedDest);
                    // Open clean link
                    if (link.target === '_blank') {
                        window.open(cleanUrl, '_blank');
                    } else {
                        window.location.href = cleanUrl;
                    }
                }
            } catch (error) {
                console.error("Router error:", error);
            }
        }
    }, true); // Use capture phase to intercept before MkDocs or other scripts
})();

TOUR_REQUIRED_FIELDS = {
    'main': ['name', 'wallpaper', 'members_number', 'vacants_number', 'basic_type', 'team_member'],
    'review': ['description',],
    'prices': ['currency', 'price', 'prepay_amount', 'tour_included_services', 'tour_excluded_services', 'air_tickets', 'cancellation_terms'],
    'gallery': ['tour_images'],
    'route': ['start_date', 'finish_date', 'start_city', 'finish_city',],
    'accommodation': ['tour_property_types', 'accomodation', 'tour_property_images'],
    'details': ['languages', 'difficulty_level', 'comfort_level', 'age_starts', 'age_ends'],
    'important': ['take_with']
}

NOT_MODERATED_FIELDS = {'is_active', 'on_moderation', 'vacants_number', 'is_draft', 'discount_starts', 'discount_finish', 'discount_in_prc', 'discount', 'sold', 'views_count'} 
CHECBOX_SET = {'is_guaranteed', 'is_active', 'postpay_on_start_day', 'scouting', 'animals_not_exploited', 'month_recurrent', 'flight_included', 'babies_alowed', 'on_moderation', 'week_recurrent', 'is_draft', 'instant_booking'}
EXCLUDED_FK_FIELDS = {'tour_basic', 'wallpaper', 'team_member', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_russian_region', 'finish_russian_region', 'start_city', 'finish_city'}


MTM_FIELDS = ['additional_types', 'tour_property_types', 'accomodation', 'tour_property_images', 'languages', 'tour_images',]
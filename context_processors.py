def family_ui(request):
    lang = getattr(request, 'family_language', request.session.get('family_language', 'sw'))
    labels = {
        'sw': {
            'dashboard':'Dashibodi', 'members':'Wanaukoo', 'payments':'Michango na malipo',
            'meetings':'Vikao', 'notices':'Matangazo', 'logout':'Toka',
            'welcome':'Karibu kwenye mfumo wa ukoo', 'overview':'Muhtasari wa shughuli za familia',
            'registered':'Wanaukoo waliosajiliwa', 'verified':'Michango iliyothibitishwa',
            'pending':'Malipo yanayosubiri', 'upcoming':'Vikao vijavyo',
            'latest_notices':'Matangazo ya hivi karibuni', 'latest_payments':'Malipo ya hivi karibuni',
            'language':'Lugha', 'swahili':'Kiswahili', 'english':'English',
        },
        'en': {
            'dashboard':'Dashboard', 'members':'Family members', 'payments':'Contributions & payments',
            'meetings':'Meetings', 'notices':'Announcements', 'logout':'Log out',
            'welcome':'Welcome to the family system', 'overview':'Family activity overview',
            'registered':'Registered family members', 'verified':'Verified contributions',
            'pending':'Payments awaiting verification', 'upcoming':'Upcoming meetings',
            'latest_notices':'Latest announcements', 'latest_payments':'Recent payments',
            'language':'Language', 'swahili':'Kiswahili', 'english':'English',
        }
    }
    return {'ui': labels.get(lang, labels['sw']), 'current_language': lang}

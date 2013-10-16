#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from litebrowser import Browser

"""
This module allows you to access the FB API from a username/password pair.
Works only with users who use facebook in Spanish, for now.
"""


def troubleshoting(browser, verbose=2):
    html = browser.get_html()
    if "www.facebook.com/messages" in html:
        if 2 < verbose: print("Logged in")
        return True
    if html.startswith("Success"):
        if 2 < verbose: print("Privileges granted")
        return True

    elif "alguien intentó iniciar sesión en tu cuenta" in html:
        if 1 < verbose: print("Suspicious session")
        browser.get_forms()[0].submit()
        return troubleshoting(browser)
    elif "Ver un intento de inicio de sesión reciente" in html:
        if 0 < verbose: print("Suspicious session, map")
        form = browser.get_forms()[0]
        browser.go(form._form.click("submit[This is Okay]"))
        return troubleshoting(browser)
    elif "Recordar navegador" in html:
        form = browser.get_forms()[0]
        form.submit()
        return troubleshoting(browser)
    elif "Tu cuenta está bloqueada temporalmente." in html:
        form = browser.get_forms()[0]
        form.submit()
        return troubleshoting(browser)
    elif "permissions_app_name" in html:
        if 0 < verbose: print("Autorizar sesión de permisos")
        form = browser.get_forms()[0]
        browser.go(form._form.click("__CONFIRM__"))
        return troubleshoting(browser)

    elif "recover/initiate" in html:
        raise ValueError("Par usuario, contraseña incorrecto.")
    elif "data-captcha-class=" in html:
        raise RuntimeError("Captcha: intervención manual requerida.")

    else:
        print("\n\n    ESTADO NO RECONOCIDO\n\n")
        browser.show()
        import IPython
        IPython.embed()
        return False


def get_token(username, password=None, appid="616893704999769"):
    url = ("""https://graph.facebook.com/oauth/authorize?client_id="""
        + appid + """&redirect_uri=http://www.facebook.com/connect/"""
        """login_success.html&type=user_agent&display=popup&scope="""
            "user_about_me,friends_about_me,user_activities,friends_activities,"
            "user_birthday,friends_birthday,user_checkins,friends_checkins,"
            "user_education_history,friends_education_history,user_events,"
            "friends_events,user_groups,friends_groups,user_hometown,friends_hometown,"
            "user_interests,friends_interests,user_likes,friends_likes,user_location,"
            "friends_location,user_notes,friends_notes,user_photos,friends_photos,"
            "user_questions,friends_questions,user_relationships,"
            "friends_relationships,user_relationship_details,"
            "friends_relationship_details,user_religion_politics,"
            "friends_religion_politics,user_status,friends_status,user_subscriptions,"
            "friends_subscriptions,user_videos,friends_videos,user_website,"
            "friends_website,user_work_history,friends_work_history,read_friendlists,"
            "read_insights,read_mailbox,read_requests,read_stream,xmpp_login,"
            "user_online_presence,friends_online_presence,ads_management,create_event,"
            "manage_friendlists,manage_notifications,publish_actions,publish_stream,"
            "rsvp_event,publish_actions,user_actions.music,friends_actions.music,"
            "user_actions.news,friends_actions.news,user_actions.video," 
            "friends_actions.video,user_games_activity,friends_games_activity,"
            "manage_pages,email"
        ) # give me the power
    if not password:
        username, password = get_credentials(username)
    browser = Browser()
    form = browser.get_forms("http://fb.com")[0]
    form["email"] = username
    form["pass"] = password
    form.submit()
    assert troubleshoting(browser)
    html = browser.get_html(url)
    assert troubleshoting(browser)
    html = browser.get_html()
    if "Success" in html:
        try:
            utoken = next((url for url in reversed(browser.hist) if "token" in url))
        except IndexError:
            import IPython
            IPython.embed()
        token = utoken.split("=")[1]
        token = token.split("&")[0]
        return token
    else:
        browser.show()
        raise ValueError("Not success")


def get_credentials(name):
    accounts = [account for account in (line.strip().split("#")[0].split(";")
        for line in open("login.txt").readlines())
            if len(account) == 3]

    d_accounts = {
        name:(username, password)
        for name, username, password in accounts}
    d_accounts.update({
        username:(username, password)
        for name, username, password in accounts})

    return d_accounts[name]


def main():
    print("import it, enjoy it.")


if __name__ == "__main__":
    exit(main()) 

import random, vk_api, vk
import urllib.request
from ast import literal_eval as make_tuple
from pathlib import Path
from PIL import Image
from markov_chain import MarkovChain
import random
import json
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from simpledemotivators import Demotivator
vk_session = vk_api.VkApi(token='c4c7a30545abf7afbb05f43aeaa0ec6d96ead40847230c41f9e514a83c5afe2d8877739d7ff38d2194ee5')
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
longpoll = VkBotLongPoll(vk_session, 212885589)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk)
first_time = False
meme_post_chance = 2
viser_chance = 5
monkey_post_chance = 2
mozhno_srat = True
obezyani = ["doc-212885589_637738641", "doc-212885589_637738657", "doc-212885589_637738671", "doc-212885589_637738700", "doc-212885589_637738723", "doc-212885589_637738737", "doc-212885589_637738856", "doc-212885589_637738862", "doc-212885589_637738873"]

tichokeywords = ["ухх", "прокоф иди нахуй",]
mc = MarkovChain()

def markov_viser():
    with open('neuroshtun.txt', 'r', encoding="utf-8") as c:
        for line in c.readlines():
            mc.parse_and_add(line.strip())
        return mc.generate_sentence(random.randint(180, 400))

def msgsend(id, text, attach):
    vk.messages.send(
        key = ("dea4d7ccceee551f288c01a8570a3370f0fc894f"),
        server = ("https://lp.vk.com/wh212885589"),
        ts=("50"),
        user_id = id,
        message = text,
        attachment=attach,
        random_id = 0
        )

def msggsend(id, text, attach):
    vk.messages.send(
        key = ("dea4d7ccceee551f288c01a8570a3370f0fc894f"),
        server = ("https://lp.vk.com/wh212885589"),
        ts=("50"),
        random_id = 0,
        message=text,
        attachment=attach,
        chat_id=id
        )

def kick(member_id, chat_id):
    vk.messages.removeChatUser(
        chat_id = chat_id,
        member_id = member_id
        )

def save_photo(url):
    all_source_imgs = list(Path('./Source Images').rglob('*'))
    number = 0
    for el in all_source_imgs:
        number += 1
    resource = urllib.request.urlopen(url)
    out = open("Source Images\\" + str(number) + ".jpg", 'wb')
    out.write(resource.read())
    out.close()


def saylog_append(userid, text, attach):
    parsed_url = " "
    saylog = open('saylog.txt', 'a', encoding="utf-8")
    learn = open('learn.txt', 'a', encoding="utf-8")
    if userid > 0:
        user_get=vk.users.get(user_ids = (userid))
        user_get=user_get[0]
        name = user_get['first_name'] + " " + user_get['last_name']
    else:
        name = 'Какой-то бот'

    print(name + ": " + text)
    for a in attach:
        if userid < 0:
            break
        if a.get('type') == 'photo':
            photo_dict = a.get('photo')
            siz = photo_dict['sizes']
            for si in siz:
                if si.get('type') == 'x':
                    if 'url' in si.keys():
                        parsed_url = si.get('url')
                        print(parsed_url)
                        save_photo(parsed_url)
                    else:
                        parsed_url = si.get('scr')
                        print(parsed_url)
                        save_photo(parsed_url)
                    break
                else:
                    continue
    if "полный хохотач" not in text.lower() and "стасян высри" not in text.lower() and "геншин" not in text.lower() and "стасян спать" not in text.lower() and "стасян ген" not in text.lower() and text != "":
        learn.write(text + "|||")
    saylog.write(name + "(" + str(userid) + ")"  + ": " + text + " " + parsed_url + '\n' + '\n')
    saylog.close()
    learn.close()
    return parsed_url

def upload_photo(upload, photo):
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key


def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )

def send_photo_chat(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        key = ("dea4d7ccceee551f288c01a8570a3370f0fc894f"),
        server = ("https://lp.vk.com/wh212885589"),
        ts=("50"),
        random_id = 0,
        attachment=attachment,
        chat_id=peer_id
        )
    
def random_viser(context):
    learnfile = open('learn.txt', 'r', encoding="utf-8")
    var_list = learnfile.read().split('|||')
    var_list.pop()
    var_list.pop()
    if context in var_list and context is not None:
        find_in_list = [index for (index, item) in enumerate(var_list) if item == context]
        previser_index = random.choice(find_in_list) + 1
        print(previser_index)
        if previser_index >= len(var_list):
            viser = random.choice(var_list)
        else:
            viser = var_list[previser_index] 
    else:
        viser = random.choice(var_list)
    if viser == "":
        viser = "Ухх!"
    learnfile.close()
    return viser.replace("стасян", "")

def demo_gen(peer_id, from_chat, src_image=None, phrase_1=None, phrase_2=None, u_url = False):
 if src_image is None:
    all_source_imgs = list(Path('./Source Images').rglob('*'))
    rand_src_img = random.choice(all_source_imgs)
    src_image = rand_src_img
 if phrase_2 is None and phrase_1 is not None:
    phrase_2 = random_viser(phrase_1)
 elif phrase_2 is None and phrase_1 is None:
    phrase_1 = random_viser(None)
    phrase_2 = random_viser(None)

 demo_filepath = Path(f'./Demo/demotivator_lol.jpg')

 demo = Demotivator(phrase_1, phrase_2)
 demo.create(src_image, result_filename=demo_filepath, use_url = u_url)

 print(demo_filepath)
 if from_chat:
        send_photo_chat(vk, peer_id, *upload_photo(upload, str(demo_filepath)))
 else:
        send_photo(vk, peer_id, *upload_photo(upload, str(demo_filepath)))

###########################МЕМ БОТ

def color2tuple(bg_info):
    if bg_info == 'w':
        return (255, 255, 255, 0)

    return None

def get_background(template, template_info):
    # If we're going not going to paste over image, we make a b/w layer
    if template_info['background'] != 'o':
        return Image.new('RGB', template.size, color2tuple(template_info['background']))
    else:
        return template

def get_unique_sources(template_info, template_num):
    """
    Gets unique source images to be used in template
    (whilst making sure it's not a duplicated meme)"""
    all_source_imgs = list(Path('./Source Images').rglob('*'))

    while True:
        src_imgs = []

        for box in template_info['boxes']:
            # If image is repeated, the source image is the same
            if 'repeat_prev' not in box:
                rand_src_img = random.choice(all_source_imgs)

            src_imgs.append(rand_src_img)

        meme_filename = f'{template_num}-{"-".join([img.stem for img in src_imgs])}.png'
        meme_filepath = Path(f'./Memes/{meme_filename}')

        # If meme has already been made -> select new src images
        # Otherwise
        return src_imgs, meme_filepath

def make_meme(bg, template, template_info, src_imgs):
    for i, box in enumerate(template_info['boxes']):
        src = Image.open(src_imgs[i])

        # Box (Blank Area)
        size_x, size_y = make_tuple(box['size'])

        # Resizes image AND keeps aspect ratio
        ## Shrink
        if src.size[0] > size_x or src.size[1] > size_y:
            src = src.resize((size_x, size_y))
        ## Enlarge
        else:
            hpercent = size_y / src.size[1]  # Magic pt. 1
            wsize = int(src.size[0] * hpercent)  # Magic 2: The Awakening
            src = src.resize((size_x, size_y))  # Magic 3: Revenge of the Syntax

            if src.size[0] > size_x :
                wpercent = size_x / src.size[0]  # Magic IV: A New Hope
                hsize = int(src.size[1] * wpercent)  # Magic 5: Wrath of Fam
                src = src.resize((size_x, size_y))  # Magic 6: The Return of the Bu

        # Coordinates of top left corner (where image is pasted)
        top_left = make_tuple(box['left_corner'])
        # Remaining space inside box (used for centering)
        blank_x = size_x - src.size[0]
        blank_y = size_y - src.size[1]

        # Pastes centered Source Image in Box
        bg.paste(src, (int(top_left[0] + blank_x / 2), int(top_left[1] + blank_y / 2)))

    # Overlay meme over background layer
    if template_info['background'] != 'o':
        bg.paste(template, (0, 0), template)

    return bg

def mememaker(peer_id, from_chat):
    with open('sizes.json') as sizes:
        jsonData = json.load(sizes)

    all_templates = list(Path('./Templates').rglob('*'))
    template_path = random.choice(all_templates)
    template_info = jsonData[template_path.stem]
    message_is_from_chat = from_chat

    template = Image.open(template_path)
    bg = get_background(template, template_info)
    src_imgs, meme_filepath = get_unique_sources(template_info, template_path.stem)
    meme = make_meme(bg, template, template_info, src_imgs)
    meme.save(meme_filepath)
    print(meme_filepath)
    if message_is_from_chat:
        send_photo_chat(vk, peer_id, *upload_photo(upload, str(meme_filepath)))
    else:
        send_photo(vk, peer_id, *upload_photo(upload, str(meme_filepath)))
        

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        image = saylog_append(event.object['from_id'], event.object['text'], (event.object['attachments']))

        if first_time:
            if event.from_user:
                    msgsend(event.object['from_id'], "Всем привет, я только что проснулся", None)
            elif event.from_chat:
                    msggsend(event.chat_id, "Всем привет, я только что проснулся", None)
            first_time = False

        if monkey_post_chance >= random.randint(1, 100):
            if event.from_user:
                  msgsend(event.object['from_id'], None,random.choice(obezyani))
            elif event.from_chat:
                  msggsend(event.chat_id, None,random.choice(obezyani))

            continue
            
        #if event.from_user:
             #msgsend(event.object['from_id'], random_viser(event.object['text']), None)

        if viser_chance >= random.randint(1, 100):
            if event.from_user:
                continue
            elif event.from_chat:
                msggsend(event.chat_id, random_viser(event.object['text']),None)

        if meme_post_chance >= random.randint(1, 100):
            if event.from_user:
                continue
            elif event.from_chat:
                 mememaker(event.chat_id, True)
                 
        for item in tichokeywords:
            if item in event.object['text'].lower():
                if event.from_user:
                    msgsend(event.object['from_id'], "Ты чё, волчара?", None)
                elif event.from_chat:
                    msggsend(event.chat_id, "Ты чё, волчара?", None)

            continue
        if "геншин" in event.object['text'].lower():
            if event.from_user:
                    msgsend(event.object['from_id'], None, "photo-212885589_457239807")
            elif event.from_chat:
                    msggsend(event.chat_id, None, "photo-212885589_457239807")

            continue


        if "полный хохотач" in event.object['text'].lower():
            if event.from_user:
                 mememaker(event.object['from_id'], False)
            elif event.object['from_id'] < 0:
                 msggsend(event.chat_id, 'Ты чё, ботяра?!',None)
            elif event.from_chat:
                if mozhno_srat:
                 mememaker(event.chat_id, True)
                else:
                 msggsend(event.chat_id, 'Ты чё, волчара, ты чё?! В лс сри, ухх!',None)

            continue

        if "стасян ген" in event.object['text'].lower():
            if image != " ":
                src = image
                u_u = True
            else:
                src = None
                u_u = False
            text = event.object['text']
            text = text.replace("стасян ген", "")
            text = text.strip()
            if text != "":
                text = text.split(';')
                if len(text) <= 1:
                    ph_1 = text[0].strip()
                    ph_2 = None
                else:
                    ph_1 = text[0].strip()
                    ph_2 = text[1].strip()
            else:
                ph_1 = None
                ph_2 = None
            if event.from_user:
                 demo_gen(event.object['from_id'], False, src_image = src, u_url = u_u, phrase_1=ph_1, phrase_2=ph_2)
            elif event.object['from_id'] < 0:
                 msggsend(event.chat_id, 'Ты чё, ботяра?!',None)
            elif event.from_chat:
                if mozhno_srat:
                 demo_gen(event.chat_id, True, src_image = src, u_url = u_u, phrase_1=ph_1, phrase_2=ph_2)
                else:
                 msggsend(event.chat_id, 'Ты чё, волчара, ты чё?! В лс сри, ухх!',None)

            continue

        if "волчар" in event.object['text'].lower():
             if event.from_user:
                  msgsend(event.object['from_id'], None,"photo-212885589_457239017")
             elif event.from_chat:
                msggsend(event.chat_id, None,"photo-212885589_457239017")

             continue

        if "максим могила" in event.object['text'].lower(): 
             if event.from_user:
                  msgsend(event.object['from_id'], None,"photo-205919831_457239212")
             elif event.from_chat:
                  msggsend(event.chat_id, None,"photo-205919831_457239212")

             continue

        if "стасян спать" in event.object['text'].lower():
            if event.object['from_id'] == 238027756:
                
                if event.from_user:
                        msgsend(event.object['from_id'], "Приятных волкснов.", None)
                elif event.from_chat:
                        msggsend(event.chat_id, "Всем приятных волкснов", None)
                break

            else:
                if event.from_user:
                        msgsend(event.object['from_id'], "Не", None)
                elif event.from_chat:
                        msggsend(event.chat_id, "Не", None)
            continue

        if "стасян можешь срать" in event.object['text'].lower():
            if event.object['from_id'] == 238027756:
                
                if event.from_user:
                        msgsend(event.object['from_id'], "=)", None)
                elif event.from_chat:
                        msggsend(event.chat_id, "=)", None)
                mozhno_srat = True

            else:
                if event.from_user:
                        msgsend(event.object['from_id'], "Не", None)
                elif event.from_chat:
                        msggsend(event.chat_id, "Не", None)
            continue

        if "няшк" in event.object['text'].lower() or "няшек" in event.object['text'].lower():
            if event.from_user:
                  msgsend(event.object['from_id'], None,"doc-212885589_635665400")
            elif event.from_chat:
                  msggsend(event.chat_id, None,"doc-212885589_635665400")

            continue

        if "стасян я запрещаю срать" in event.object['text'].lower():
            if event.object['from_id'] == 238027756:
                
                if event.from_user:
                        msgsend(event.object['from_id'], "=(", None)
                elif event.from_chat:
                        msggsend(event.chat_id, "=(", None)
                mozhno_srat = False

            else:
                if event.from_user:
                        msgsend(event.object['from_id'], "Не", None)
                elif event.from_chat:
                        msggsend(event.chat_id, "Не", None)

            continue
        
        if "стасян бань" in event.object['text'].lower():
            if event.from_user:
                continue
            elif event.from_chat:
                msggsend(event.chat_id, None, "doc-212885589_635664183")
                try:
                    kick("160531707", event.chat_id)
                except:
                    msggsend(event.chat_id, "А где?", "doc-212885589_635665400")

            continue

        if "нейроштун" in event.object['text'].lower():
            if event.from_user:
                 continue
            elif event.object['from_id'] < 0:
                 msggsend(event.chat_id, 'Тут только ты срешь, ботяра.',None)
            elif event.from_chat:
                msggsend(event.chat_id, markov_viser(),None)

            continue

        if "обезьян" in event.object['text'].lower():
            if event.from_user:
                  msgsend(event.object['from_id'], None,random.choice(obezyani))
            elif event.from_chat:
                  msggsend(event.chat_id, None,random.choice(obezyani))

            continue
            

        if "стасян " in event.object['text'].lower():
            if event.from_user:
                 continue
            elif event.object['from_id'] < 0:
                 msggsend(event.chat_id, 'Тут только ты срешь, ботяра.',None)
            elif event.from_chat:
                msggsend(event.chat_id, random_viser(event.object['text'].replace("стасян", "").lower()),None)

from sooslwww.models import BodyLocationCircle, BodyLocationEllipse, BodyLocationRectangle, BodyLocationPolygon, BodyLocationPolygonPoint, BodyHeadLocationType

def body_locations():
    return [

    ('500', ['Fingers', 'contact', 'polygon'],
    [(8, -248), (30.5, -238), (26.5, -232), (2.5, -240)],                 [5.0, 504.0]),


    ('508', ['Back of Fingers', 'contact', 'polygon', 'behind'],
    [(8, -248), (30.5, -238), (26.5, -232), (2.5, -240)],
    [15.0, 505.0]),

    ('510', ['Front of Hand (Palm)', 'contact', 'circle'],
    [(25, -225), 18],
    [-4.0, 460.0]),

    ('518', ['Back of Hand', 'contact', 'circle', 'behind'],
    [(8, -179), 15],
    [27.0, 420.0]),

    ('520', ['Wrist', 'contact', 'circle'],
    [(200, -208), 12],
    [1.0, 434.0]),

    ('528', ['Back of Wrist', 'contact', 'circle', 'behind'],
    [(210, -169), 12],
    [-18.0, 402.0]),

    ('530', ['Lower Arm', 'contact', 'polygon'],
    [(170, -198), (185, -201), (198, -172), (190, -169)],
    [7.0, 396.0]),

    ('538', ['Inner Elbow', 'contact', 'circle'],
    [(172, -156), 16],
    [-1.0, 334.0]),

    ('540', ['Outer Elbow', 'contact', 'circle', 'behind'],
    [(163, -166), 11],
    [-3.0, 354]),

    ('548', ['Upper Arm', 'contact', 'polygon'],
    [(154, -130), (162, -161), (172, -112), (159, -108)],
    [9.0, 286.0]),

    ('550', ['Armpit (left)', 'contact', 'ellipse'],
    [(143, -130), (12, 18)],
    [9.0, 267.0]),

    ('558', ['Armpit (right)', 'contact', 'ellipse'],
    [(0.0, 0.0), (12, 18)],
    [76.0, 138.0]),

    ('560', ['Shoulder (left)', 'contact', 'circle'],
    [(154, -99), 23],
    [-8.0, 211.0]),

    ('568', ['Shoulder (right)', 'contact', 'circle'],
    [(0.0, 0.0), 23],
    [67.0, 113.0]),

    ('570', ['Top of Shoulder (left)', 'contact', 'ellipse'],
    [(124, -88), (30, 8)],
    [13.0, 190.0]),

    ('578', ['Top of Shoulder (right)', 'contact', 'ellipse'],
    [(0.0, 0.0), (30, 8)],
    [67.0, 103.0]),

    ('580', ['Above Shoulder (left)', 'spatial', 'ellipse'],
    [(130, -78), (28, 8)],
    [9.0, 168.0]),

    ('588', ['Above Shoulder (right)', 'spatial', 'ellipse'],
    [(0.0, 0.0), (28, 8)],
    [66.0, 91.0]),

    ('590', ['Hip (left)', 'contact', 'ellipse'],
    [(0, 0), (12, 45)],
    [147.0, 205.0]),

    ('598', ['Hip (right)', 'contact', 'ellipse'],
    [(0, 0), (12, 45)],
    [81.0, 205.0]),

    ('5a0', ['Lower Torso', 'contact', 'polygon'],
    [(83, -117), (80, -176), (147, -176), (144, -117)],
    [6.0, 321.0]),

    ('5a8', ['Chest (right)', 'contact', 'polygon'],
    [(75, -123), (99, -123), (99, -91), (80, -91)],
    [7.0, 234.0]),

    ('5b0', ['Chest (center)', 'contact', 'polygon'],
    [(101, -123), (124, -123), (124, -91), (101, -91)],
    [7.0, 234.0]),

    ('5b8', ['Chest (left)', 'contact', 'polygon'],
    [(126, -123), (150, -123), (145, -91), (126, -91)],
    [7.0, 234.0]),

    ('5c0', ['Neck', 'contact', 'rectangle'],
    [(99, -81), (25, 10)],
    [7.0, 177.0]),

    ('5c8', ['Low Side of Head (left)', 'spatial', 'ellipse'],
    [(140, -66), (10, 30)],
    [7.0, 123.0]),

    ('5d0', ['Low Side of Head (right)', 'spatial', 'ellipse'],
    [(0.0, 0.0), (10, 30)],
    [77.0, 58.0]),

    ('5d8', ['High Side of Head (left)', 'spatial', 'ellipse'],
    [(140, -34), (10, 30)],
    [7.0, 56.0]),

    ('5e0', ['High Side of Head (right)', 'spatial', 'ellipse'],
    [(0.0, 0.0), (10, 30)],
    [77.0, 23.0]),

    ('5e8', ['Above Head', 'spatial', 'ellipse'],
    [(86, 7), (48, 8)],
    [7.0, 9.0]),

    ('5f0', ['Above Front of Head', 'spatial', 'ellipse'],
    [(86, -1), (48, 8)],
    [7.0, 8.0]),

    ('0', ['Head', 'contact', 'ellipse'],
    [(91, -63), (40, 55)],
    [6.0, 94.0])

    ]

def head_locations():
    return [

    ('5f8', ['Chin', 'contact', 'ellipse'],
    [(103, 33), (28, 15)],
    [144.0, 108.0]),

    ('600', ['Lips', 'contact', 'ellipse'],
    [(93.5, 51), (48, 26)],
    [146.0, 60.0]),


    ('608', ['Teeth', 'contact', 'polygon'],
    [(96, 66.3), (104, 62.85), (109, 62.06), (109, 66.3), (109, 62.06), (114, 61.65), (116.5, 61.6), (116.5, 66.3), (116.5, 61.6), (119, 61.75), (124, 62.06), (124, 66.3), (124, 62.06), (129, 62.95), (137, 66.3)],
    [147.0, 55.0]),

    ('610', ['Tongue', 'contact', 'ellipse'],
    [(104, 55), (28, 8)],
    [146.0, 70.0]),

    ('618', ['Nose', 'contact', 'polygon'],
    [(106, 115), (112, 95), (118, 95), (124, 115)],
    [145.0, -13.0]),

    ('620', ['Cheek (left)', 'contact', 'circle'],
    [(144, 95), 25],
    [134.0, -7.0]),

    ('628', ['Cheek (right)', 'contact', 'circle'],
    [(0.0, 0.0), 25],
    [220.0, 89.0]),

    ('630', ['Ear (left)', 'contact', 'ellipse'],
    [(52, 91), (11, 20)],
    [259.0, -6.0]),

    ('638', ['Ear (right)', 'contact', 'ellipse'],
    [(0.0, 0.0), (11, 20)],
    [203.0, 87.0]),

    ('640', ['Eye (left)', 'contact', 'ellipse'],
    [(85.5, 114), (16, 11)],
    [187.0, -44.0]),

    ('648', ['Eye (right)', 'contact', 'ellipse'],
    [(85.5, 114), (16, 11)],
    [146.0, -45.0]),

    ('650', ['Eyebrow (left)', 'contact', 'polygon'],
    [(77, 131), (96, 131), (110, 138), (81, 134)],
    [190.0, -73.0]),

    ('658', ['Eyebrow (right)', 'contact', 'polygon'],
    [(77, 138), (89, 135), (108, 134), (106, 131), (93, 130), (82, 133)],
    [147.0, -73.0]),

    ('660', ['Temple (left)', 'contact', 'ellipse'],
    [(0.0, 0.0), (10, 30)],
    [302.0, 27.0]),

    ('668', ['Temple (right)', 'contact', 'ellipse'],
    [(64, 148), (10, 30)],
    [147.0, -122.0]),

    ('670', ['Forehead', 'contact', 'ellipse'],
    [(79, 152), (75, 27)],
    [145.0, -131.0]),

    ('678', ['Top of Head', 'contact', 'ellipse'],
    [(79, 178), (75, 12)],
    [144.0, -171.0]),

    ('680', ['Back of Head', 'contact', 'ellipse', 'behind'],
    [(15, 135), (136, 96)],
    [178.0, -141.0])
    ]

def AddPart(part, on_head):
    code, strings, data, pos = part
    x_offset = pos[0]
    y_offset = pos[1]

    if 'ellipse' in strings:
	part = BodyLocationEllipse()

	top_left_x = data[0][0] + x_offset
	top_left_y = data[0][1] + y_offset
	width = data[1][0]
	height = data[1][1]

	part.center_x=top_left_x+width/2
	part.center_y=top_left_y+height/2
	part.radius_x=width/2
	part.radius_y=height/2

    elif 'circle' in strings:
	part = BodyLocationCircle()
	top_left_x = data[0][0] + x_offset
	top_left_y = data[0][1] + y_offset
	radius = data[1]/2

	part.center_x=top_left_x+radius
	part.center_y=top_left_y+radius
	part.radius=radius

    elif 'polygon' in strings:
	part = BodyLocationPolygon()

    elif 'rectangle' in strings:
	part = BodyLocationRectangle()
	top_left_x = data[0][0] + x_offset
	top_left_y = data[0][1] + y_offset
	width = data[1][0]
	height = data[1][1]

	part.x = top_left_x
	part.y = top_left_y
	part.width = width
	part.height = height

    #Common data
    part.text=strings[0]
    part.behind = ('behind' in strings)
    part.on_head = on_head
    part.type = BodyHeadLocationType.objects.get(text=strings[1])
    part.save()

    if 'polygon' in strings:
	for polygon in data:
	    point = BodyLocationPolygonPoint()
	    point.x = polygon[0] + x_offset
	    point.y = polygon[1] + y_offset
	    point.polygon = part
	    point.save()


def ImportBodyParts():
    body_location = body_locations()
    for part in body_location:
	AddPart(part, False)

    head_location = head_locations()
    for part in head_location:
	AddPart(part, True)

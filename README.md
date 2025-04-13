![cover image](media/cover.png)

# 🏀 Hands-Off-My-Ball

_This lil' baller keeps dodging your hand 👋_

![hover preview](media/result.gif)

---

### How it’s made

- Built voxel characters in **MagicaVoxel**, exported as `.obj`
- Imported to **Blender** for animation (13-frame hover cycle)
  [image](media/blender_insert_keyframe.png)
- Exported position & quaternion rotation for each frame
- Reconstructed characters in **Pyglet** using custom `body_objects.json`
- Assembled parts via cubes in `CustomGroup` (BodyPart, Ball, Hand)
  [image](media/T_pose.png)
- Played animations with quaternions
- Used `AnimationManager` to switch states on mouse hover

---

_Every quaternion here tells a story._ 🥹

---

`#blender` `#pyglet` `#animation` `#voxel` `#quaternion` `#interactive`

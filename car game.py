
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APEX - Rocket Supercar Racing</title>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>

<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
    overflow:hidden;
    background:#05080e;
    color:white;
    font-family:Arial,sans-serif;
}
canvas{display:block}

#hud{
    position:absolute;
    inset:0;
    pointer-events:none;
}
.top{
    display:flex;
    justify-content:space-between;
    padding:25px 35px;
}
.logo{
    font-size:28px;
    font-weight:900;
    letter-spacing:5px;
}
.logo span{color:#00e5ff}

.panel{
    background:rgba(5,12,22,.8);
    border:1px solid rgba(255,255,255,.15);
    backdrop-filter:blur(8px);
    padding:13px 20px;
    border-radius:12px;
}
.stats{display:flex;gap:10px}
.stat small{
    display:block;
    color:#9daebd;
    font-size:10px;
    letter-spacing:2px;
}
.stat strong{
    display:block;
    font-size:23px;
    margin-top:5px;
}
#level,#speed,#score{color:#00e5ff}

.bottom{
    position:absolute;
    bottom:25px;
    left:35px;
    right:35px;
    display:flex;
    justify-content:space-between;
    align-items:end;
}
#progress{
    width:220px;
    height:6px;
    background:#273342;
    margin-top:10px;
    border-radius:10px;
    overflow:hidden;
}
#progressFill{
    height:100%;
    width:0%;
    background:#00e5ff;
}
#controls{
    color:#b5c4d1;
    font-size:12px;
    line-height:2;
    text-align:right;
}
#nitro{
    color:#00e5ff;
    font-weight:bold;
    margin-top:8px;
}

#screen{
    position:absolute;
    inset:0;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(120deg,rgba(1,5,13,.93),rgba(1,12,25,.65));
    z-index:5;
}
.card{
    text-align:center;
    padding:45px;
    width:min(520px,90%);
    background:rgba(8,17,30,.9);
    border:1px solid rgba(255,255,255,.18);
    border-radius:18px;
    box-shadow:0 20px 100px #000;
}
.card h1{
    font-size:clamp(38px,7vw,65px);
    letter-spacing:5px;
}
.card h1 span{color:#00e5ff}
.card p{
    color:#aab8c8;
    margin:17px 0 25px;
    line-height:1.8;
}
button{
    border:0;
    padding:15px 35px;
    color:#001018;
    background:#00e5ff;
    font-size:14px;
    font-weight:bold;
    letter-spacing:2px;
    border-radius:6px;
    cursor:pointer;
}
button:hover{background:white}

#message{
    font-size:13px;
    color:#00e5ff;
    margin-top:20px;
}
#mobile{
    display:none;
    position:absolute;
    bottom:100px;
    left:0;
    right:0;
    justify-content:space-between;
    padding:15px;
    pointer-events:auto;
}
#mobile button{
    padding:18px;
    margin:4px;
}
#boost{background:#ffb300}

@media(max-width:700px){
    .top{padding:12px}
    .bottom{left:12px;right:12px;bottom:12px}
    .panel{padding:9px}
    .stat strong{font-size:16px}
    #mobile{display:flex}
    #controls{display:none}
}
</style>
</head>

<body>

<div id="hud">
    <div class="top">
        <div class="logo">APEX<span>.</span></div>
        <div class="stats">
            <div class="panel stat">
                <small>LEVEL</small>
                <strong id="level">01</strong>
            </div>
            <div class="panel stat">
                <small>KM/H</small>
                <strong id="speed">000</strong>
            </div>
            <div class="panel stat">
                <small>SCORE</small>
                <strong id="score">0000</strong>
            </div>
        </div>
    </div>

    <div class="bottom">
        <div class="panel">
            <small id="stage">SNOW MOUNTAIN</small>
            <div id="progress"><div id="progressFill"></div></div>
            <small id="distance">0 / 1000 M</small>
            <div id="carName" style="margin-top:10px;font-weight:bold">
                APEX GT
            </div>
            <div id="nitro">🚀 ROCKET MODE READY</div>
        </div>

        <div id="controls">
            W / ↑ ACCELERATE<br>
            S / ↓ BRAKE<br>
            A / ← LEFT<br>
            D / → RIGHT<br>
            SPACE NITRO BOOST
        </div>
    </div>
</div>

<div id="mobile">
    <div>
        <button id="left">◀</button>
        <button id="right">▶</button>
    </div>
    <div>
        <button id="brake">BRAKE</button>
        <button id="accelerate">GO</button>
        <button id="boost">🚀</button>
    </div>
</div>

<div id="screen">
    <div class="card">
        <h1>APEX<span>.</span></h1>
        <p>
            THE ULTIMATE ROCKET SUPERCAR EXPERIENCE<br>
            SNOW. MUD. HIGHWAY.<br>
            THREE LEVELS. THREE MACHINES.
        </p>
        <button id="start">START RACING</button>
        <div id="message">ARE YOU READY?</div>
    </div>
</div>

<script type="module">
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

// GAME SETTINGS

const TOTAL_DISTANCE = 1000;

const LEVELS = [
    {
        name:"SNOW MOUNTAIN",
        car:"APEX GT",
        color:0x08bce8,
        maxSpeed:500
    },
    {
        name:"MUDDY OFF-ROAD",
        car:"STORM X",
        color:0xff3030,
        maxSpeed:650
    },
    {
        name:"HIGHWAY EXTREME",
        car:"PHANTOM RS",
        color:0xffc400,
        maxSpeed:800
    }
];

let scene,camera,renderer,car;
let wheels=[];
let obstacles=[];

let distance=0;
let speed=0;
let score=0;
let scoreFraction=0;

let level=0;
let running=false;
let nitro=false;
let steer=0;
let lastTime=0;

// Prevents awarding level bonuses more than once.
let levelBonus=[false,false,false];

const keys={};
const loader=new GLTFLoader();

// THREE JS INITIALIZATION

function init(){

    scene=new THREE.Scene();

    scene.background=new THREE.Color(0x9ab5c8);
    scene.fog=new THREE.Fog(0x9ab5c8,80,350);

    camera=new THREE.PerspectiveCamera(
        65,
        window.innerWidth/window.innerHeight,
        0.1,
        1500
    );

    camera.position.set(0,5,12);

    renderer=new THREE.WebGLRenderer({
        antialias:false,
        powerPreference:"high-performance"
    });

    renderer.setSize(window.innerWidth,window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio,1));
    renderer.shadowMap.enabled=false;
    renderer.outputColorSpace=THREE.SRGBColorSpace;

    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xffffff,0x344455,2));

    const sun=new THREE.DirectionalLight(0xffffff,2);
    sun.position.set(-30,60,30);
    scene.add(sun);

    createWorld();
    createCar();
    createObstacles();

    window.addEventListener("resize",resize);

    animate(0);
}

// MATERIALS

function material(color){
    return new THREE.MeshStandardMaterial({
        color:color,
        roughness:0.8
    });
}

function cube(w,h,d,x,y,z,color,parent=scene){

    const mesh=new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d),
        material(color)
    );

    mesh.position.set(x,y,z);
    parent.add(mesh);

    return mesh;
}

// ENVIRONMENTS

function createWorld(){

    const ground=new THREE.Mesh(
        new THREE.PlaneGeometry(400,1600),
        material(0x65746c)
    );

    ground.rotation.x=-Math.PI/2;
    ground.position.set(0,-0.2,-500);
    scene.add(ground);

    const zones=[
        {start:0,length:300,road:0xdde8ed,ground:0xb8d4e8},
        {start:300,length:350,road:0x514638,ground:0x51412e},
        {start:650,length:350,road:0x292d35,ground:0x313b49}
    ];

    zones.forEach((zone,i)=>{

        const road=new THREE.Mesh(
            new THREE.PlaneGeometry(16,zone.length),
            material(zone.road)
        );

        road.rotation.x=-Math.PI/2;
        road.position.set(0,0.01,-zone.start-zone.length/2);
        scene.add(road);

        const terrain=new THREE.Mesh(
            new THREE.PlaneGeometry(400,zone.length),
            material(zone.ground)
        );

        terrain.rotation.x=-Math.PI/2;
        terrain.position.set(0,-0.1,-zone.start-zone.length/2);
        scene.add(terrain);

        for(const side of [-1,1]){
            cube(
                0.35,0.4,zone.length,
                side*8.2,0.2,
                -zone.start-zone.length/2,
                0xeeeeee
            );
        }

        for(let j=0;j<8;j++){

            const z=-zone.start-j*(zone.length/8)-8;
            const side=j%2===0?-1:1;

            if(i===0){

                const mountain=new THREE.Mesh(
                    new THREE.ConeGeometry(14,25,5),
                    material(0xd5e5ef)
                );

                mountain.position.set(side*27,10,z);
                scene.add(mountain);

            }else if(i===1){

                const rock=new THREE.Mesh(
                    new THREE.DodecahedronGeometry(2),
                    material(0x665342)
                );

                rock.position.set(side*15,1,z);
                scene.add(rock);

            }else{

                cube(1,1.2,5,side*10,0.6,z,0x64717e);

            }
        }
    });
}

// SUPERCAR CREATION

function createCar(){

    car=new THREE.Group();
    scene.add(car);

    buildCar(LEVELS[0].color);

    car.position.set(0,0,0);
}

function buildCar(color){

    car.clear();
    wheels=[];

    const bodyMat=new THREE.MeshPhysicalMaterial({
        color:color,
        metalness:0.8,
        roughness:0.22,
        clearcoat:1
    });

    function part(geo,mat,x,y,z){

        const m=new THREE.Mesh(geo,mat);
        m.position.set(x,y,z);
        car.add(m);

        return m;
    }

    // Main body
    part(
        new THREE.BoxGeometry(2.3,0.48,4.5),
        bodyMat,0,0.65,0
    );

    // Hood
    part(
        new THREE.BoxGeometry(2.15,0.22,1.45),
        bodyMat,0,0.91,-1.45
    );

    // Cabin
    const glass=new THREE.MeshStandardMaterial({
        color:0x101f32,
        metalness:0.7,
        roughness:0.15
    });

    part(
        new THREE.BoxGeometry(1.55,0.68,1.85),
        glass,0,1.15,0.15
    );

    // Front bumper
    part(
        new THREE.BoxGeometry(2.5,0.12,0.55),
        material(0x111111),0,0.42,-2.2
    );

    // Rear spoiler
    part(
        new THREE.BoxGeometry(2.2,0.12,0.35),
        material(0x151515),0,1.25,1.95
    );

    // Headlights
    const lightMat=new THREE.MeshBasicMaterial({
        color:0x9deeff
    });

    part(
        new THREE.BoxGeometry(0.55,0.09,0.08),
        lightMat,-0.75,0.78,-2.25
    );

    part(
        new THREE.BoxGeometry(0.55,0.09,0.08),
        lightMat,0.75,0.78,-2.25
    );

    // Wheels
    for(const x of [-1.12,1.12]){
        for(const z of [-1.45,1.45]){

            const wheel=new THREE.Mesh(
                new THREE.CylinderGeometry(0.43,0.43,0.28,16),
                material(0x101010)
            );

            wheel.rotation.z=Math.PI/2;
            wheel.position.set(x,0.45,z);

            car.add(wheel);
            wheels.push(wheel);
        }
    }
}

// BLENDER MODEL SUPPORT

async function loadBlenderCar(index){

    const files=[
        "level1.glb",
        "level2.glb",
        "level3.glb"
    ];

    try{

        const gltf=await loader.loadAsync(
            "/static/models/"+files[index]
        );

        if(index!==level || !running)return;

        car.clear();

        const model=gltf.scene;
        model.scale.setScalar(1);

        model.traverse(obj=>{
            if(obj.isMesh){
                obj.castShadow=false;
                obj.receiveShadow=false;
            }
        });

        car.add(model);

    }catch(error){

        console.log("Using built-in supercar.");

    }
}

// OBSTACLES

function createObstacles(){

    for(let i=0;i<15;i++){

        const z=-20-i*55;
        const x=(Math.random()>0.5?1:-1)*(2+Math.random()*4);

        const obstacle=new THREE.Group();

        cube(
            1.5,1.5,2,
            0,0.8,0,
            i%2===0?0xff3030:0x667788,
            obstacle
        );

        obstacle.position.set(x,0,z);

        scene.add(obstacle);
        obstacles.push(obstacle);
    }
}

// SCORE DISPLAY

function updateScoreDisplay(){

    document.getElementById("score").textContent =
        score.toLocaleString("en-IN");
}

// ADD SCORE OVER TIME

function addDrivingScore(dt){

    let pointsPerSecond=10;

    // Nitro has the highest scoring rate.
    if(nitro && (keys["arrowup"] || keys["w"])){

        pointsPerSecond=50;

    }else if(speed>=300){

        pointsPerSecond=25;

    }

    scoreFraction+=pointsPerSecond*dt;

    const wholePoints=Math.floor(scoreFraction);

    if(wholePoints>0){

        score+=wholePoints;
        scoreFraction-=wholePoints;
    }
}

// LEVEL COMPLETION BONUSES

function checkLevelBonuses(){

    if(distance>=300 && !levelBonus[0]){

        levelBonus[0]=true;
        score+=500;

        showMessage("LEVEL 1 COMPLETED! +500 POINTS");
    }

    if(distance>=650 && !levelBonus[1]){

        levelBonus[1]=true;
        score+=500;

        showMessage("LEVEL 2 COMPLETED! +500 POINTS");
    }

    if(distance>=TOTAL_DISTANCE && !levelBonus[2]){

        levelBonus[2]=true;
        score+=500;

        showMessage("LEVEL 3 COMPLETED! +500 POINTS");
    }
}

// MESSAGE

function showMessage(message){

    document.getElementById("message").textContent=message;
}

// LEVEL UPGRADE

function updateLevel(){

    const newLevel=
        distance<300?0:
        distance<650?1:2;

    if(newLevel!==level){

        level=newLevel;

        const config=LEVELS[level];

        buildCar(config.color);
        loadBlenderCar(level);

        speed=Math.min(speed,config.maxSpeed);

        const backgrounds=[
            0x9ab5c8,
            0x806f59,
            0x263c56
        ];

        scene.background.setHex(backgrounds[level]);
        scene.fog.color.setHex(backgrounds[level]);

        document.getElementById("level").textContent=
            "0"+(level+1);

        document.getElementById("stage").textContent=config.name;
        document.getElementById("carName").textContent=config.car;

        showMessage("NEW SUPERCAR UNLOCKED: "+config.car);
    }
}

// KEYBOARD CONTROLS

window.addEventListener("keydown",e=>{

    keys[e.key.toLowerCase()]=true;

    if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "]
    .includes(e.key)){
        e.preventDefault();
    }

});

window.addEventListener("keyup",e=>{
    keys[e.key.toLowerCase()]=false;
});

// MOBILE CONTROLS

function bindButton(id,key){

    const btn=document.getElementById(id);

    btn.addEventListener("pointerdown",e=>{
        e.preventDefault();
        keys[key]=true;
    });

    ["pointerup","pointerleave","pointercancel"].forEach(event=>{
        btn.addEventListener(event,()=>{
            keys[key]=false;
        });
    });
}

bindButton("left","arrowleft");
bindButton("right","arrowright");
bindButton("accelerate","arrowup");
bindButton("brake","arrowdown");
bindButton("boost"," ");

// COLLISION DETECTION

function checkCollision(){

    for(const obstacle of obstacles){

        const dx=Math.abs(
            car.position.x-obstacle.position.x
        );

        const dz=Math.abs(
            car.position.z-obstacle.position.z
        );

        if(dx<1.7 && dz<2.7 && speed>10){

            speed*=0.45;

            score=Math.max(0,score-50);

            obstacle.position.z=-3000;
        }
    }
}

// ROCKET GAME MOVEMENT

function update(dt){

    if(!running)return;

    const config=LEVELS[level];

    const accelerating=
        keys["w"]||keys["arrowup"];

    const braking=
        keys["s"]||keys["arrowdown"];

    nitro=keys[" "]||keys["boost"];

    // ROCKET ACCELERATION

    if(accelerating){

        speed+=180*dt;

    }else{

        speed-=15*dt;

    }

    // NITRO BOOST

    if(nitro && accelerating){

        speed+=300*dt;

    }

    if(braking){

        speed-=120*dt;

    }

    speed=THREE.MathUtils.clamp(
        speed,0,config.maxSpeed
    );

    // STEERING

    const direction=
        (keys["a"]||keys["arrowleft"]?-1:0)+
        (keys["d"]||keys["arrowright"]?1:0);

    steer=THREE.MathUtils.lerp(
        steer,direction,dt*6
    );

    car.position.x+=
        steer*dt*(8+speed*0.05);

    car.position.x=THREE.MathUtils.clamp(
        car.position.x,-6.4,6.4
    );

    // ROAD MOVEMENT

    const movement=speed*dt*0.45;

    car.position.z-=movement;
    distance+=movement;

    // NEW SCORING SYSTEM

    if(accelerating && speed>0){

        addDrivingScore(dt);
    }

    // Level completion rewards

    checkLevelBonuses();

    // Wheel rotation

    wheels.forEach(w=>{
        w.rotation.x+=movement*0.5;
    });

    // Camera follow

    const targetCamera=new THREE.Vector3(
        car.position.x*0.55,
        5,
        car.position.z+11
    );

    camera.position.lerp(
        targetCamera,dt*4
    );

    camera.lookAt(
        car.position.x,1,car.position.z-5
    );

    checkCollision();

    updateLevel();

    // HUD

    document.getElementById("speed").textContent=
        String(Math.round(speed)).padStart(3,"0");

    updateScoreDisplay();

    document.getElementById("distance").textContent=
        Math.floor(distance)+" / "+TOTAL_DISTANCE+" M";

    document.getElementById("progressFill").style.width=
        Math.min(100,distance/TOTAL_DISTANCE*100)+"%";

    document.getElementById("nitro").textContent=
        nitro&&accelerating?
        "🚀 NITRO BOOST ACTIVE":
        "🚀 ROCKET MODE READY";

    // FINISH LINE

    if(distance>=TOTAL_DISTANCE){

        winGame();
    }
}

// ANIMATION

function animate(time){

    requestAnimationFrame(animate);

    const dt=Math.min(
        (time-lastTime)/1000||0,
        0.04
    );

    lastTime=time;

    update(dt);

    renderer.render(scene,camera);
}

// GAME START

function startGame(){

    distance=0;
    speed=0;
    score=0;
    scoreFraction=0;
    level=0;
    steer=0;
    nitro=false;
    running=true;

    levelBonus=[false,false,false];

    // Clear old key presses
    Object.keys(keys).forEach(key=>{
        keys[key]=false;
    });

    car.position.set(0,0,0);

    obstacles.forEach((o,i)=>{
        o.position.z=-20-i*55;
    });

    buildCar(LEVELS[0].color);
    loadBlenderCar(0);

    scene.background.setHex(0x9ab5c8);
    scene.fog.color.setHex(0x9ab5c8);

    document.getElementById("level").textContent="01";
    document.getElementById("speed").textContent="000";
    document.getElementById("stage").textContent=LEVELS[0].name;
    document.getElementById("carName").textContent=LEVELS[0].car;
    document.getElementById("distance").textContent="0 / 1000 M";
    document.getElementById("progressFill").style.width="0%";
    document.getElementById("nitro").textContent="🚀 ROCKET MODE READY";

    updateScoreDisplay();

    document.getElementById("screen").style.display="none";
}

// VICTORY

function winGame(){

    if(!running)return;

    running=false;

    // Championship bonus
    score+=2000;

    updateScoreDisplay();

    document.getElementById("screen").style.display="flex";

    document.querySelector(".card h1").innerHTML=
        "YOU <span>WIN!</span>";

    document.querySelector(".card p").innerHTML=
        "ALL THREE LEVELS COMPLETED<br>"+
        "FINAL SCORE: "+score.toLocaleString("en-IN")+"<br>"+
        "YOU ARE THE APEX CHAMPION.<br><br>"+
        "🏆 NEW SUPERCAR UNLOCKED: PHANTOM RS";

    document.getElementById("start").textContent=
        "RACE AGAIN";

    showMessage("CHAMPIONSHIP BONUS: +2000 POINTS");
}

// START BUTTON

document.getElementById("start").addEventListener("click",()=>{

    document.querySelector(".card h1").innerHTML=
        "APEX<span>.</span>";

    document.querySelector(".card p").innerHTML=
        "THE ULTIMATE ROCKET SUPERCAR EXPERIENCE<br>"+
        "SNOW. MUD. HIGHWAY.<br>"+
        "THREE LEVELS. THREE MACHINES.";

    startGame();

});

// RESIZE

function resize(){

    camera.aspect=window.innerWidth/window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );
}

init();

</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=False, threaded=True)

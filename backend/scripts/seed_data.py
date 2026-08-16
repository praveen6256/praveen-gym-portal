"""
Seed the database with workout plans and food data.
Run after creating the admin account.

Usage:
  cd backend
  python scripts/seed_data.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# ─── MALE WORKOUT PLANS ────────────────────────────────────────────────────

MALE_WORKOUTS = [
    {
        "day": "monday",
        "gender": "male",
        "focus": "Chest & Triceps",
        "description": "Build a powerful chest and strong triceps with this push-day session.",
        "exercises": [
            {
                "name": "Barbell Bench Press",
                "description": "Lie flat on a bench, grip the bar slightly wider than shoulder-width. Lower the bar to your chest, then press back up explosively.",
                "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80",
                "sets": 4, "reps": 10, "rest_seconds": 90, "muscle_group": "Chest",
            },
            {
                "name": "Incline Dumbbell Press",
                "description": "Set bench to 30–45°. Press dumbbells from chest level upward, focusing on upper chest activation.",
                "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 75, "muscle_group": "Upper Chest",
            },
            {
                "name": "Cable Chest Flyes",
                "description": "Stand between cable pulleys at shoulder height. Bring handles together in an arc motion, squeezing chest at the peak.",
                "image_url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 60, "muscle_group": "Chest",
            },
            {
                "name": "Tricep Rope Pushdown",
                "description": "Attach rope to cable. Keep elbows fixed at sides, push rope down and outward until arms are fully extended.",
                "image_url": "https://images.unsplash.com/photo-1547919307-1ecb10702e6f?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 60, "muscle_group": "Triceps",
            },
            {
                "name": "Skull Crushers",
                "description": "Lie on a bench holding an EZ bar. Lower bar toward your forehead by bending elbows, then extend arms back up.",
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 60, "muscle_group": "Triceps",
            },
        ],
    },
    {
        "day": "tuesday",
        "gender": "male",
        "focus": "Back & Biceps",
        "description": "Develop a wide, thick back paired with well-defined biceps.",
        "exercises": [
            {
                "name": "Pull-Ups",
                "description": "Grip bar with hands wider than shoulders. Pull body up until chin clears the bar, lower slowly.",
                "image_url": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=600&q=80",
                "sets": 4, "reps": 8, "rest_seconds": 90, "muscle_group": "Back/Lats",
            },
            {
                "name": "Barbell Bent-Over Row",
                "description": "Hinge at hips, keep back flat. Pull bar to lower chest, squeezing shoulder blades together.",
                "image_url": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=600&q=80",
                "sets": 4, "reps": 10, "rest_seconds": 90, "muscle_group": "Mid Back",
            },
            {
                "name": "Seated Cable Row",
                "description": "Sit at cable machine, pull handle to abdomen keeping chest up and back straight.",
                "image_url": "https://images.unsplash.com/photo-1584863231364-2edc166de576?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 75, "muscle_group": "Back",
            },
            {
                "name": "Barbell Bicep Curl",
                "description": "Stand straight, curl bar from hip level to chin level. Keep elbows pinned to sides.",
                "image_url": "https://images.unsplash.com/photo-1550977616-efc580084ac5?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 60, "muscle_group": "Biceps",
            },
            {
                "name": "Hammer Curls",
                "description": "Hold dumbbells with neutral grip, curl up keeping palms facing each other throughout.",
                "image_url": "https://images.unsplash.com/photo-1583454155184-870a1f63aebc?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 60, "muscle_group": "Biceps/Brachialis",
            },
        ],
    },
    {
        "day": "wednesday",
        "gender": "male",
        "focus": "Legs & Glutes",
        "description": "Build strong, powerful legs with this comprehensive lower body session.",
        "exercises": [
            {
                "name": "Barbell Back Squat",
                "description": "Place bar on upper back, squat down until thighs are parallel to floor, drive through heels to stand.",
                "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=600&q=80",
                "sets": 5, "reps": 8, "rest_seconds": 120, "muscle_group": "Quads/Glutes",
            },
            {
                "name": "Romanian Deadlift",
                "description": "Hold bar at hip level, hinge forward keeping back flat and bar close to legs. Feel hamstring stretch, then drive hips forward.",
                "image_url": "https://images.unsplash.com/photo-1567598508481-65985588e295?w=600&q=80",
                "sets": 4, "reps": 10, "rest_seconds": 90, "muscle_group": "Hamstrings/Glutes",
            },
            {
                "name": "Leg Press",
                "description": "Sit in leg press machine, place feet shoulder-width apart. Lower weight until knees are at 90°, press back.",
                "image_url": "https://images.unsplash.com/photo-1517344884509-a0c97ec11bcc?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 90, "muscle_group": "Quads",
            },
            {
                "name": "Walking Lunges",
                "description": "Step forward, lower back knee toward floor. Alternate legs while walking forward.",
                "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600&q=80",
                "sets": 3, "reps": 20, "rest_seconds": 75, "muscle_group": "Quads/Glutes",
            },
            {
                "name": "Calf Raises",
                "description": "Stand on edge of step, raise heels as high as possible, lower slowly.",
                "image_url": "https://images.unsplash.com/photo-1549060279-7e168fcee0c2?w=600&q=80",
                "sets": 4, "reps": 20, "rest_seconds": 45, "muscle_group": "Calves",
            },
        ],
    },
    {
        "day": "thursday",
        "gender": "male",
        "focus": "Shoulders & Core",
        "description": "Develop boulder shoulders and a rock-solid core.",
        "exercises": [
            {
                "name": "Barbell Overhead Press",
                "description": "Press bar from shoulder height overhead. Keep core tight and avoid arching lower back.",
                "image_url": "https://images.unsplash.com/photo-1532029837206-abbe2b7620e3?w=600&q=80",
                "sets": 4, "reps": 8, "rest_seconds": 90, "muscle_group": "Shoulders",
            },
            {
                "name": "Dumbbell Lateral Raises",
                "description": "Raise dumbbells out to the sides until arms are parallel to floor. Lower under control.",
                "image_url": "https://images.unsplash.com/photo-1595078475328-1ab05d0a6a0e?w=600&q=80",
                "sets": 4, "reps": 15, "rest_seconds": 60, "muscle_group": "Side Delts",
            },
            {
                "name": "Face Pulls",
                "description": "Pull cable attachment to face level, flaring elbows out. Great for rear delt health.",
                "image_url": "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 60, "muscle_group": "Rear Delts",
            },
            {
                "name": "Plank",
                "description": "Hold straight-body position on forearms and toes. Keep hips level, breathe steadily.",
                "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=600&q=80",
                "sets": 3, "duration_minutes": 1, "rest_seconds": 45, "muscle_group": "Core",
            },
            {
                "name": "Cable Woodchops",
                "description": "Rotate torso pulling cable diagonally across body. Engages obliques and rotational core.",
                "image_url": "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 45, "muscle_group": "Obliques",
            },
        ],
    },
    {
        "day": "friday",
        "gender": "male",
        "focus": "Full Body Power",
        "description": "End the week strong with compound movements targeting every major muscle group.",
        "exercises": [
            {
                "name": "Deadlift",
                "description": "Pull bar from floor to hip height, keeping back straight and chest up. The king of compound lifts.",
                "image_url": "https://images.unsplash.com/photo-1534367610401-9f5ed68180aa?w=600&q=80",
                "sets": 4, "reps": 6, "rest_seconds": 120, "muscle_group": "Full Body",
            },
            {
                "name": "Dumbbell Thrusters",
                "description": "Squat down holding dumbbells at shoulders, then drive up and press overhead in one fluid motion.",
                "image_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&q=80",
                "sets": 4, "reps": 10, "rest_seconds": 90, "muscle_group": "Full Body",
            },
            {
                "name": "Kettlebell Swings",
                "description": "Hinge at hips, swing kettlebell to chest height using hip drive. Powerful posterior chain movement.",
                "image_url": "https://images.unsplash.com/photo-1517343985841-f8b2d66e010b?w=600&q=80",
                "sets": 4, "reps": 15, "rest_seconds": 60, "muscle_group": "Posterior Chain",
            },
            {
                "name": "Box Jumps",
                "description": "Explosively jump onto a box, land softly with knees slightly bent, step back down.",
                "image_url": "https://images.unsplash.com/photo-1590487988256-9ed24133863e?w=600&q=80",
                "sets": 3, "reps": 10, "rest_seconds": 75, "muscle_group": "Legs/Power",
            },
            {
                "name": "Battle Ropes",
                "description": "Alternate arm waves for conditioning and upper body endurance.",
                "image_url": "https://images.unsplash.com/photo-1507398941214-572c25a4f7f2?w=600&q=80",
                "sets": 3, "duration_minutes": 1, "rest_seconds": 60, "muscle_group": "Conditioning",
            },
        ],
    },
    {
        "day": "saturday",
        "gender": "male",
        "focus": "Arms & Cardio",
        "description": "Pump up the arms and finish the week with conditioning work.",
        "exercises": [
            {
                "name": "EZ Bar Curl",
                "description": "Curl EZ bar from hip level, focusing on bicep peak contraction.",
                "image_url": "https://images.unsplash.com/photo-1583454155184-870a1f63aebc?w=600&q=80",
                "sets": 4, "reps": 12, "rest_seconds": 60, "muscle_group": "Biceps",
            },
            {
                "name": "Tricep Dips",
                "description": "Lower body between parallel bars until upper arm is parallel to floor, press back up.",
                "image_url": "https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=600&q=80",
                "sets": 4, "reps": 12, "rest_seconds": 60, "muscle_group": "Triceps",
            },
            {
                "name": "Concentration Curl",
                "description": "Sit on bench, rest elbow on inner thigh, curl dumbbell for maximum bicep isolation.",
                "image_url": "https://images.unsplash.com/photo-1550977616-efc580084ac5?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 45, "muscle_group": "Biceps",
            },
            {
                "name": "Overhead Tricep Extension",
                "description": "Hold dumbbell overhead with both hands, lower behind head and extend back up.",
                "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 45, "muscle_group": "Triceps",
            },
            {
                "name": "Treadmill Intervals",
                "description": "20 min: 2 min easy, 1 min sprint, repeat. Burns fat and builds cardiovascular endurance.",
                "image_url": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&q=80",
                "sets": 1, "duration_minutes": 20, "rest_seconds": 0, "muscle_group": "Cardio",
            },
        ],
    },
]

# ─── FEMALE WORKOUT PLANS ──────────────────────────────────────────────────

FEMALE_WORKOUTS = [
    {
        "day": "monday",
        "gender": "female",
        "focus": "Glutes & Lower Body",
        "description": "Sculpt and strengthen your glutes, hamstrings, and quads with this lower body blast.",
        "exercises": [
            {
                "name": "Hip Thrusts",
                "description": "Place upper back on bench, drive hips upward using glutes. Squeeze at the top for 1 second.",
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&q=80",
                "sets": 4, "reps": 15, "rest_seconds": 75, "muscle_group": "Glutes",
            },
            {
                "name": "Sumo Squat",
                "description": "Wide stance, toes pointed outward. Squat down keeping chest tall, great for inner thighs and glutes.",
                "image_url": "https://images.unsplash.com/photo-1609899464424-5c0568bd5dcc?w=600&q=80",
                "sets": 4, "reps": 15, "rest_seconds": 60, "muscle_group": "Glutes/Inner Thighs",
            },
            {
                "name": "Romanian Deadlift",
                "description": "Hinge at hips, lower dumbbells along legs, feeling hamstring stretch. Drive hips forward to stand.",
                "image_url": "https://images.unsplash.com/photo-1567598508481-65985588e295?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 75, "muscle_group": "Hamstrings/Glutes",
            },
            {
                "name": "Glute Kickbacks (Cable)",
                "description": "Attach ankle cuff to cable. Kick leg straight back, squeezing glute at top.",
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&q=80",
                "sets": 3, "reps": 20, "rest_seconds": 45, "muscle_group": "Glutes",
            },
            {
                "name": "Lateral Band Walks",
                "description": "Place resistance band around ankles, step sideways maintaining squat position.",
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&q=80",
                "sets": 3, "reps": 20, "rest_seconds": 45, "muscle_group": "Glute Medius/Abductors",
            },
        ],
    },
    {
        "day": "tuesday",
        "gender": "female",
        "focus": "Upper Body & Toning",
        "description": "Tone arms, shoulders, and back for a lean and defined upper body.",
        "exercises": [
            {
                "name": "Dumbbell Shoulder Press",
                "description": "Press dumbbells from shoulder height overhead. Core tight, avoid overarching back.",
                "image_url": "https://images.unsplash.com/photo-1532029837206-abbe2b7620e3?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 60, "muscle_group": "Shoulders",
            },
            {
                "name": "Lateral Raises",
                "description": "Raise dumbbells out to sides with slight bend in elbows. Control the lowering phase.",
                "image_url": "https://images.unsplash.com/photo-1595078475328-1ab05d0a6a0e?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 45, "muscle_group": "Side Delts",
            },
            {
                "name": "Seated Cable Row",
                "description": "Pull cable to abdomen, squeezing shoulder blades. Great for posture and back definition.",
                "image_url": "https://images.unsplash.com/photo-1584863231364-2edc166de576?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 60, "muscle_group": "Back",
            },
            {
                "name": "Bicep Curls",
                "description": "Curl dumbbells with controlled motion. Avoid swinging body.",
                "image_url": "https://images.unsplash.com/photo-1550977616-efc580084ac5?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 45, "muscle_group": "Biceps",
            },
            {
                "name": "Tricep Pushdowns",
                "description": "Push cable down until arms are fully extended. Excellent arm toner.",
                "image_url": "https://images.unsplash.com/photo-1547919307-1ecb10702e6f?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 45, "muscle_group": "Triceps",
            },
        ],
    },
    {
        "day": "wednesday",
        "gender": "female",
        "focus": "Core & Flexibility",
        "description": "Strengthen your core, improve posture, and enhance flexibility with this midweek session.",
        "exercises": [
            {
                "name": "Plank",
                "description": "Hold straight-body position on forearms. Breathe steadily. Essential for core stability.",
                "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=600&q=80",
                "sets": 3, "duration_minutes": 1, "rest_seconds": 45, "muscle_group": "Core",
            },
            {
                "name": "Dead Bug",
                "description": "Lie on back, extend opposite arm and leg while keeping lower back pressed to floor.",
                "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 45, "muscle_group": "Core Stability",
            },
            {
                "name": "Russian Twists",
                "description": "Sit with knees bent, lean back slightly, rotate torso side to side. Add dumbbell for progression.",
                "image_url": "https://images.unsplash.com/photo-1600881333168-2ef49b341f30?w=600&q=80",
                "sets": 3, "reps": 20, "rest_seconds": 45, "muscle_group": "Obliques",
            },
            {
                "name": "Yoga Flow (Sun Salutation)",
                "description": "5 rounds of sun salutation sequence to improve mobility, reduce stiffness, and connect breath to movement.",
                "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&q=80",
                "sets": 1, "duration_minutes": 10, "rest_seconds": 0, "muscle_group": "Full Body Flexibility",
            },
            {
                "name": "Glute Bridge",
                "description": "Lie on back, feet flat on floor, drive hips up squeezing glutes at top.",
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&q=80",
                "sets": 3, "reps": 20, "rest_seconds": 45, "muscle_group": "Glutes/Core",
            },
        ],
    },
    {
        "day": "thursday",
        "gender": "female",
        "focus": "Legs & Cardio",
        "description": "Tone legs and get heart rate up with this energetic cardio and lower body combo.",
        "exercises": [
            {
                "name": "Goblet Squat",
                "description": "Hold dumbbell at chest, squat deep keeping chest up and knees tracking over toes.",
                "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=600&q=80",
                "sets": 4, "reps": 15, "rest_seconds": 60, "muscle_group": "Quads/Glutes",
            },
            {
                "name": "Step-Ups",
                "description": "Step onto a bench or box, drive through heel to stand tall. Alternate legs.",
                "image_url": "https://images.unsplash.com/photo-1590487988256-9ed24133863e?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 60, "muscle_group": "Glutes/Quads",
            },
            {
                "name": "Jumping Jacks",
                "description": "Explosive full-body cardio movement to elevate heart rate.",
                "image_url": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&q=80",
                "sets": 3, "duration_minutes": 2, "rest_seconds": 45, "muscle_group": "Cardio",
            },
            {
                "name": "Leg Curl (Machine)",
                "description": "Lie face down on machine, curl legs upward focusing on hamstring contraction.",
                "image_url": "https://images.unsplash.com/photo-1517344884509-a0c97ec11bcc?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 60, "muscle_group": "Hamstrings",
            },
            {
                "name": "Jump Rope",
                "description": "Skip rope for fat burning and coordination. Great low-impact cardio finisher.",
                "image_url": "https://images.unsplash.com/photo-1507398941214-572c25a4f7f2?w=600&q=80",
                "sets": 1, "duration_minutes": 10, "rest_seconds": 0, "muscle_group": "Cardio",
            },
        ],
    },
    {
        "day": "friday",
        "gender": "female",
        "focus": "Full Body Sculpt",
        "description": "A complete sculpting session hitting all major muscle groups for a strong finish to the week.",
        "exercises": [
            {
                "name": "Dumbbell Squat to Press",
                "description": "Squat holding dumbbells at shoulders, stand and press overhead in one fluid motion.",
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&q=80",
                "sets": 4, "reps": 12, "rest_seconds": 75, "muscle_group": "Full Body",
            },
            {
                "name": "Dumbbell Row",
                "description": "Brace on bench, pull dumbbell to hip, keeping back flat. Great for back and biceps.",
                "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 60, "muscle_group": "Back/Biceps",
            },
            {
                "name": "Reverse Lunges",
                "description": "Step backward, lower back knee to floor. Less knee stress than forward lunges.",
                "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600&q=80",
                "sets": 3, "reps": 12, "rest_seconds": 60, "muscle_group": "Glutes/Quads",
            },
            {
                "name": "Push-Ups",
                "description": "Perform full or modified push-ups, keeping body straight. Builds chest, shoulders, and core.",
                "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80",
                "sets": 3, "reps": 15, "rest_seconds": 60, "muscle_group": "Chest/Shoulders",
            },
            {
                "name": "Ab Wheel Rollout",
                "description": "Roll wheel forward from kneeling position, extending body. Roll back using core strength.",
                "image_url": "https://images.unsplash.com/photo-1600881333168-2ef49b341f30?w=600&q=80",
                "sets": 3, "reps": 10, "rest_seconds": 60, "muscle_group": "Core",
            },
        ],
    },
    {
        "day": "saturday",
        "gender": "female",
        "focus": "Cardio & Active Recovery",
        "description": "Boost metabolism with enjoyable cardio and soothing stretches.",
        "exercises": [
            {
                "name": "Elliptical / Cycling",
                "description": "30 minutes at moderate intensity. Great for cardiovascular health without joint impact.",
                "image_url": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&q=80",
                "sets": 1, "duration_minutes": 30, "rest_seconds": 0, "muscle_group": "Cardio",
            },
            {
                "name": "Bodyweight Squats",
                "description": "High-rep bodyweight squats to maintain leg activation without heavy loading.",
                "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=600&q=80",
                "sets": 3, "reps": 25, "rest_seconds": 45, "muscle_group": "Legs",
            },
            {
                "name": "Deep Stretching Routine",
                "description": "Hip flexor stretch, hamstring stretch, quad stretch, shoulder stretch — 60 sec each side.",
                "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&q=80",
                "sets": 1, "duration_minutes": 15, "rest_seconds": 0, "muscle_group": "Flexibility",
            },
            {
                "name": "Foam Rolling",
                "description": "Roll quads, IT band, glutes, and upper back. Reduces soreness and improves recovery.",
                "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600&q=80",
                "sets": 1, "duration_minutes": 10, "rest_seconds": 0, "muscle_group": "Recovery",
            },
        ],
    },
]

# ─── FOOD DATABASE ─────────────────────────────────────────────────────────

FOODS = [
    # Proteins
    {"name": "Chicken Breast", "category": "protein", "calories_per_100g": 165, "protein_g": 31, "carbs_g": 0, "fat_g": 3.6, "fiber_g": 0, "dietary_tags": [], "description": "Lean protein source, ideal for muscle building and weight management.", "serving_suggestion": "Grill with olive oil and herbs. Pair with rice and vegetables."},
    {"name": "Eggs", "category": "protein", "calories_per_100g": 155, "protein_g": 13, "carbs_g": 1.1, "fat_g": 11, "fiber_g": 0, "dietary_tags": ["vegetarian"], "description": "Complete protein with all essential amino acids. Extremely versatile.", "serving_suggestion": "Boil, scramble, or poach. Perfect pre/post workout."},
    {"name": "Paneer", "category": "protein", "calories_per_100g": 265, "protein_g": 18, "carbs_g": 3.4, "fat_g": 20, "fiber_g": 0, "dietary_tags": ["vegetarian"], "description": "High-protein Indian cheese, great for vegetarians.", "serving_suggestion": "Grill or add to curries. High in calcium too."},
    {"name": "Tuna (canned)", "category": "protein", "calories_per_100g": 116, "protein_g": 26, "carbs_g": 0, "fat_g": 1, "fiber_g": 0, "dietary_tags": [], "description": "Very high protein, very low fat. Excellent for cutting phases.", "serving_suggestion": "Mix with Greek yogurt or add to salads."},
    {"name": "Greek Yogurt", "category": "protein", "calories_per_100g": 59, "protein_g": 10, "carbs_g": 3.6, "fat_g": 0.4, "fiber_g": 0, "dietary_tags": ["vegetarian"], "description": "Probiotic-rich protein snack with low sugar content.", "serving_suggestion": "Top with berries and a drizzle of honey."},
    {"name": "Lentils (Dal)", "category": "protein", "calories_per_100g": 116, "protein_g": 9, "carbs_g": 20, "fat_g": 0.4, "fiber_g": 7.9, "dietary_tags": ["vegetarian", "vegan"], "description": "Protein and fiber powerhouse for vegetarians and vegans.", "serving_suggestion": "Cook as dal, add to soups, or use in salads."},
    {"name": "Salmon", "category": "protein", "calories_per_100g": 208, "protein_g": 20, "carbs_g": 0, "fat_g": 13, "fiber_g": 0, "dietary_tags": [], "description": "Rich in omega-3 fatty acids and high-quality protein.", "serving_suggestion": "Bake with lemon and dill. Serve with sweet potato."},
    {"name": "Chickpeas", "category": "protein", "calories_per_100g": 164, "protein_g": 8.9, "carbs_g": 27, "fat_g": 2.6, "fiber_g": 7.6, "dietary_tags": ["vegetarian", "vegan"], "description": "Plant-based protein with excellent fiber content.", "serving_suggestion": "Roast for a crunchy snack or add to salads and curries."},
    # Carbohydrates
    {"name": "Brown Rice", "category": "carbohydrate", "calories_per_100g": 111, "protein_g": 2.6, "carbs_g": 23, "fat_g": 0.9, "fiber_g": 1.8, "dietary_tags": ["vegetarian", "vegan"], "description": "Complex carb with better nutritional profile than white rice.", "serving_suggestion": "Use as base for bowls. Combine with dal or stir-fry vegetables."},
    {"name": "Oats", "category": "carbohydrate", "calories_per_100g": 389, "protein_g": 17, "carbs_g": 66, "fat_g": 7, "fiber_g": 10.6, "dietary_tags": ["vegetarian", "vegan"], "description": "Slow-release energy with beta-glucan for heart health.", "serving_suggestion": "Overnight oats, porridge, or blended into smoothies."},
    {"name": "Sweet Potato", "category": "carbohydrate", "calories_per_100g": 86, "protein_g": 1.6, "carbs_g": 20, "fat_g": 0.1, "fiber_g": 3, "dietary_tags": ["vegetarian", "vegan"], "description": "Nutrient-dense carb rich in beta-carotene and potassium.", "serving_suggestion": "Bake whole or cut into wedges. Great pre-workout fuel."},
    {"name": "Whole Wheat Bread", "category": "carbohydrate", "calories_per_100g": 247, "protein_g": 13, "carbs_g": 41, "fat_g": 3.4, "fiber_g": 6, "dietary_tags": ["vegetarian"], "description": "Higher fiber alternative to white bread.", "serving_suggestion": "Use for sandwiches with eggs, avocado, or peanut butter."},
    {"name": "Banana", "category": "carbohydrate", "calories_per_100g": 89, "protein_g": 1.1, "carbs_g": 23, "fat_g": 0.3, "fiber_g": 2.6, "dietary_tags": ["vegetarian", "vegan"], "description": "Quick-release carbs with potassium. Excellent pre-workout snack.", "serving_suggestion": "Eat 30–45 mins before workout. Add to smoothies or oat bowls."},
    {"name": "Quinoa", "category": "carbohydrate", "calories_per_100g": 120, "protein_g": 4.4, "carbs_g": 22, "fat_g": 1.9, "fiber_g": 2.8, "dietary_tags": ["vegetarian", "vegan"], "description": "Complete protein grain — contains all essential amino acids.", "serving_suggestion": "Use as rice substitute. Mix into salads or grain bowls."},
    # Fats
    {"name": "Almonds", "category": "fat", "calories_per_100g": 579, "protein_g": 21, "carbs_g": 22, "fat_g": 50, "fiber_g": 12.5, "dietary_tags": ["vegetarian", "vegan"], "description": "Rich in healthy monounsaturated fats, Vitamin E and magnesium.", "serving_suggestion": "Handful as snack. Add to oatmeal or yogurt."},
    {"name": "Avocado", "category": "fat", "calories_per_100g": 160, "protein_g": 2, "carbs_g": 9, "fat_g": 15, "fiber_g": 6.7, "dietary_tags": ["vegetarian", "vegan"], "description": "Heart-healthy monounsaturated fats with potassium and folate.", "serving_suggestion": "Spread on toast, add to salads, or blend into smoothies."},
    {"name": "Olive Oil", "category": "fat", "calories_per_100g": 884, "protein_g": 0, "carbs_g": 0, "fat_g": 100, "fiber_g": 0, "dietary_tags": ["vegetarian", "vegan"], "description": "Anti-inflammatory monounsaturated fat, staple of Mediterranean diet.", "serving_suggestion": "Use for cooking or as salad dressing. Keep quantities small."},
    {"name": "Peanut Butter", "category": "fat", "calories_per_100g": 588, "protein_g": 25, "carbs_g": 20, "fat_g": 50, "fiber_g": 6, "dietary_tags": ["vegetarian", "vegan"], "description": "Calorie-dense with protein and healthy fats. Great for muscle gain.", "serving_suggestion": "2 tbsp on whole wheat toast or added to protein shakes."},
    {"name": "Walnuts", "category": "fat", "calories_per_100g": 654, "protein_g": 15, "carbs_g": 14, "fat_g": 65, "fiber_g": 6.7, "dietary_tags": ["vegetarian", "vegan"], "description": "High in omega-3 ALA, excellent for brain and heart health.", "serving_suggestion": "Snack on 5–7 walnut halves. Add to salads or oatmeal."},
    # Fiber/Vegetables
    {"name": "Broccoli", "category": "fiber", "calories_per_100g": 34, "protein_g": 2.8, "carbs_g": 7, "fat_g": 0.4, "fiber_g": 2.6, "dietary_tags": ["vegetarian", "vegan"], "description": "Cruciferous vegetable with vitamins C & K, folate and fiber.", "serving_suggestion": "Steam or roast. Add to stir-fries, pasta, or eat as side dish."},
    {"name": "Spinach", "category": "fiber", "calories_per_100g": 23, "protein_g": 2.9, "carbs_g": 3.6, "fat_g": 0.4, "fiber_g": 2.2, "dietary_tags": ["vegetarian", "vegan"], "description": "Iron and vitamin-rich leafy green with very low calories.", "serving_suggestion": "Add raw to salads, blend in smoothies, or wilt into curries."},
    {"name": "Apples", "category": "fiber", "calories_per_100g": 52, "protein_g": 0.3, "carbs_g": 14, "fat_g": 0.2, "fiber_g": 2.4, "dietary_tags": ["vegetarian", "vegan"], "description": "High in pectin fiber and antioxidants. Great for gut health.", "serving_suggestion": "Eat with peanut butter or slice into yogurt bowls."},
    {"name": "Flaxseeds", "category": "fiber", "calories_per_100g": 534, "protein_g": 18, "carbs_g": 29, "fat_g": 42, "fiber_g": 27, "dietary_tags": ["vegetarian", "vegan"], "description": "Extremely high fiber with omega-3 and lignans for hormonal health.", "serving_suggestion": "Add 1 tbsp ground flaxseed to smoothies, oats, or yogurt daily."},
]


async def seed():
    mongo_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DATABASE_NAME", "praveen_gym")

    if not mongo_url:
        print("❌ MONGODB_URL not set in .env file")
        return

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    print("[SEED] Seeding workout plans...")
    await db.workouts.delete_many({})  # Clear existing
    all_workouts = MALE_WORKOUTS + FEMALE_WORKOUTS
    if all_workouts:
        result = await db.workouts.insert_many(all_workouts)
        print(f"   [OK] Inserted {len(result.inserted_ids)} workout plans")

    print("[SEED] Seeding food database...")
    await db.foods.delete_many({})
    if FOODS:
        for f in FOODS:
            f["created_at"] = datetime.now(timezone.utc)
        result = await db.foods.insert_many(FOODS)
        print(f"   [OK] Inserted {len(result.inserted_ids)} food items")

    print("\n[SUCCESS] Database seeded successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())

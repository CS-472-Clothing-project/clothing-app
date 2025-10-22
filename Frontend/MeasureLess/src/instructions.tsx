// instructions.tsx
// Setup & Instructions page: visual cards, environment/clothing guidance,
// privacy note (server-side processing, no human review), and a CTA to camera.

import { FaCamera, FaTshirt, FaRulerCombined, FaUserShield, FaMobileAlt, FaAngleDoubleUp } from "react-icons/fa";
import SideMenu from "./components/SideMenu";

export default function Instructions() {
  // Small UI helpers to keep JSX readable
  const Section = ({ title, children }: { title: string; children: React.ReactNode }) => (
    <section className="max-w-3xl w-full bg-card border rounded-xl p-5 md:p-6 shadow-sm">
      <h2 className="text-xl md:text-2xl font-semibold mb-3">{title}</h2>
      <div className="space-y-3 text-sm md:text-base">{children}</div>
    </section>
  );

  const Bullet = ({ children }: { children: React.ReactNode }) => (
    <li className="flex items-start gap-3">
      <span className="mt-1.5 h-2 w-2 rounded-full bg-foreground/50" />
      <span>{children}</span>
    </li>
  );

  const Card = ({ icon, title, text }:{
    icon: React.ReactNode; title: string; text: string;
  }) => (
    <div className="flex items-start gap-3 p-4 border rounded-lg bg-secondary">
      <div className="text-2xl shrink-0">{icon}</div>
      <div>
        <div className="font-medium">{title}</div>
        <div className="text-sm opacity-80">{text}</div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen w-full flex justify-center">
      <main className="w-full max-w-5xl px-4 md:px-8 py-6 md:py-10 space-y-6">
        {/* Global nav */}
        <SideMenu />

        <h1 className="text-2xl md:text-3xl font-bold">Setup & Instructions</h1>

        {/* Quick visual tips */}
        <div className="grid md:grid-cols-3 gap-4">
          <Card icon={<FaCamera />} title="Prop Phone @ 90°" text="Use a desk or tripod. Keep the camera vertical and stable—no hand-holding." />
          <Card icon={<FaTshirt />} title="Wear Tight Clothing" text="Tight shirt or sportswear. Avoid loose/flowy items and jackets." />
          <Card icon={<FaRulerCombined />} title="Stand Back" text="Stand far enough to fit your full body in frame (about 6–8 ft)." />
        </div>

        <Section title="Environment">
          <ul className="space-y-2">
            <Bullet>Use a plain background if possible (door, wall, closet).</Bullet>
            <Bullet>Even lighting; avoid strong backlight and harsh shadows.</Bullet>
            <Bullet>Phone around waist–chest height, facing straight on (90°).</Bullet>
            <Bullet>Keep head-to-feet in frame with a little space above/below.</Bullet>
          </ul>
        </Section>

        <Section title="Clothing Guidelines">
          <ul className="space-y-2">
            <Bullet>Upper: shirtless or tight-fitting top preferred; avoid loose tops.</Bullet>
            <Bullet>Lower: leggings/spandex or shorts; avoid long skirts/dresses/baggy pants.</Bullet>
            <Bullet>Remove items that change silhouette (coats, backpacks, long scarves).</Bullet>
          </ul>

          {/* Extra tips */}
          <div className="grid md:grid-cols-2 gap-3 mt-3">
            <Card icon={<FaAngleDoubleUp />} title="Hair & Accessories" text="Tie long hair up; remove hats. Avoid bulky accessories that hide body contours." />
            <Card icon={<FaMobileAlt />} title="Phone Placement" text="Camera should be upright (portrait), not tilted. Don’t angle up or down." />
          </div>
        </Section>

        <Section title="Privacy & Data">
          <div className="flex items-start gap-3">
            <div className="text-2xl"><FaUserShield /></div>
            <p className="text-sm md:text-base">
              Your photos are sent securely to our measurement server and processed automatically by our algorithms.
              They aren’t reviewed by people—<strong>your images and body data never reach human eyes.</strong>
              We only use them to compute your measurements.
            </p>
          </div>
        </Section>

        <Section title="When You’re Ready">
          <ol className="list-decimal ml-6 space-y-2">
            <li>Set the phone on a desk/tripod, vertical at 90°.</li>
            <li>Stand 6–8 ft away; center yourself fully in frame.</li>
            <li>Arms relaxed at your sides; look straight ahead.</li>
            <li>Tap <strong>Get Measured</strong> to continue.</li>
          </ol>
          <div className="pt-3">
            {/* Link to the camera page */}
            <a href="/takePicture.tsx" className="inline-block px-5 py-2 rounded-lg bg-foreground text-background">
              Get Measured
            </a>
          </div>
        </Section>
      </main>
    </div>
  );
}

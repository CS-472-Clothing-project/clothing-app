import { FaCamera, FaTshirt, FaRulerCombined, FaUserShield, FaMobileAlt, FaAngleDoubleUp } from "react-icons/fa";

export default function Instructions() {
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

  const Card = ({
    icon,
    title,
    text,
  }: {
    icon: React.ReactNode;
    title: string;
    text: string;
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
        <header className="flex items-center justify-between">
          <h1 className="text-2xl md:text-3xl font-bold">Setup & Instructions</h1>
          {/* placeholder for a future menu*/}
          <div className="text-lg opacity-60">☰</div>
        </header>

        {}
        <div className="grid md:grid-cols-3 gap-4">
          <Card
            icon={<FaCamera />}
            title="Prop Phone @ 90°"
            text="Use a desk or tripod. Keep the camera vertical and stable—no hand-holding."
          />
          <Card
            icon={<FaTshirt />}
            title="Wear Tight Clothing"
            text="Tight shirt or sportswear. Avoid loose/flowy items and jackets."
          />
          <Card
            icon={<FaRulerCombined />}
            title="Stand Back"
            text="Stand far enough to fit your full body in frame (about 6–8 ft)."
          />
        </div>

        <Section title="Environment">
          <ul className="space-y-2">
            <Bullet>Use a plain background if possible (door, wall, closet).</Bullet>
            <Bullet>Bright, even lighting. Avoid strong backlight and harsh shadows.</Bullet>
            <Bullet>Place your phone on a stable surface or tripod at about waist–chest height, lens facing you straight on (90°).</Bullet>
            <Bullet>Keep the entire body visible: head to feet, with a bit of space above your head and below your feet.</Bullet>
          </ul>
        </Section>

        <Section title="Clothing Guidelines">
          <ul className="space-y-2">
            <Bullet>Upper body: shirtless or tight-fitting top preferred; avoid loose clothing.</Bullet>
            <Bullet>Lower body: leggings/spandex or shorts; avoid long skirts, dresses, or baggy pants.</Bullet>
            <Bullet>Remove items that change silhouette (coats, backpacks, scarves, long necklaces).</Bullet>
          </ul>

          <div className="grid md:grid-cols-2 gap-3 mt-3">
            <Card
              icon={<FaAngleDoubleUp />}
              title="Hair & Accessories"
              text="Tie long hair up; remove hats. Avoid bulky accessories that hide body contours."
            />
            <Card
              icon={<FaMobileAlt />}
              title="Phone Placement"
              text="Camera should be upright (portrait), not tilted. Don’t angle up or down."
            />
          </div>
        </Section>

        <Section title="Privacy & Data">
          <div className="flex items-start gap-3">
            <div className="text-2xl"><FaUserShield /></div>
            <p className="text-sm md:text-base">
              Your measurements are computed on-device. We don’t send images or body data to the cloud.
              Photos are processed locally and can be discarded after measurement.
            </p>
          </div>
        </Section>

        <Section title="When You’re Ready">
          <ol className="list-decimal ml-6 space-y-2">
            <li>Set the phone on a desk/tripod, vertical at 90°.</li>
            <li>Stand 6–8 ft away; center yourself fully in frame.</li>
            <li>Keep arms relaxed at your sides; look straight ahead.</li>
            <li>Tap Get Measured to continue.</li>
          </ol>
          <div className="pt-3">
            <a href="/takePicture.tsx" className="inline-block px-5 py-2 rounded-lg bg-foreground text-background">
              Get Measured
            </a>
          </div>
        </Section>
      </main>
    </div>
  );
}

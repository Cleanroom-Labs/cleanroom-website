import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-slate-800/70 backdrop-blur-[2px] text-text-secondary py-8 border-t border-slate-700">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="font-semibold text-text-primary">Cleanroom Labs</p>
            <p className="text-sm">
              Free and open source tools that respect privacy
            </p>
          </div>
          <div className="flex gap-6">
            <a
              href="https://github.com/cleanroom-labs"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-emerald transition-colors"
            >
              GitHub
            </a>
            {/* Donate link hidden — re-enable when ready */}
            <a
              href="mailto:lead@cleanroomlabs.dev"
              className="hover:text-emerald transition-colors"
            >
              Contact
            </a>
          </div>
        </div>
        <div className="mt-8 pt-4 border-t border-slate-700 text-center text-sm text-text-muted">
          <p>
            &copy; {new Date().getFullYear()} Cleanroom Labs. All rights
            reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}

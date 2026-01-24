import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="font-semibold text-white">Cleanroom Labs</p>
            <p className="text-sm">Free and open source tools for air-gapped development</p>
          </div>
          <div className="flex gap-6">
            <a
              href="https://github.com/cleanroom-labs"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              GitHub
            </a>
            <Link href="/donate" className="hover:text-white transition-colors">
              Donate
            </Link>
            <a
              href="mailto:lead@cleanroomlabs.dev"
              className="hover:text-white transition-colors"
            >
              Contact
            </a>
          </div>
        </div>
        <div className="mt-8 pt-4 border-t border-gray-700 text-center text-sm">
          <p>&copy; {new Date().getFullYear()} Cleanroom Labs. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}

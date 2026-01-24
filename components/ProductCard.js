export default function ProductCard({ name, description, color }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div
        className="h-32 flex items-center justify-center"
        style={{ backgroundColor: color }}
      >
        <span className="text-white text-lg font-semibold">{name}</span>
      </div>
      <div className="p-6">
        <h3 className="text-xl font-bold mb-2">{name}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}

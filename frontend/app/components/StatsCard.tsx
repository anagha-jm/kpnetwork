interface Props {
  title: string;
  value: number;
}

export default function StatsCard({
  title,
  value
}: Props) {
  return (
    <div className="border rounded-lg p-6 shadow bg-white">
      <h2 className="text-lg font-semibold">
        {title}
      </h2>

      <p className="text-4xl font-bold mt-4">
        {value}
      </p>
    </div>
  );
}
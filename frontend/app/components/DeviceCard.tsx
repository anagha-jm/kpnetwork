interface Props {
  title: string;
  value: string | number;
}

export default function DeviceCard({ title, value }: Props) {
  return (
    <div className="border rounded-lg p-4 shadow">
      <h3 className="font-bold">{title}</h3>
      <p>{value}</p>
    </div>
  );
}
CREATE TABLE houses (
    id INT PRIMARY KEY IDENTITY(1,1),
    property VARCHAR(255),
    location VARCHAR(255),
    price INT,
    type VARCHAR(255)
);


INSERT INTO houses (property, location, price, type)
VALUES
  ('Cottage by the lake', 'Lake Tahoe, California', 750000, 'Cozy'),
  ('Modern apartment', 'New York, New York', 1200000, 'Urban'),
  ('Beachfront condo', 'Malibu, California', 950000, 'Scenic'),
  ('Mountain cabin', 'Aspen, Colorado', 850000, 'Rustic'),
  ('Penthouse suite', 'Chicago, Illinois', 1300000, 'Luxury'),
  ('Historic mansion', 'Savannah, Georgia', 1500000, 'Elegant'),
  ('Suburban home', 'Austin, Texas', 600000, 'Family-friendly'),
  ('Country farmhouse', 'Nashville, Tennessee', 700000, 'Charming'),
  ('City loft', 'San Francisco, California', 1100000, 'Modern'),
  ('Eco-friendly house', 'Portland, Oregon', 800000, 'Sustainable');
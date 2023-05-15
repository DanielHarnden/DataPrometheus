CREATE TABLE IF NOT EXISTS albums (
	AlbumId INTEGER,
	Title NVARCHAR(160),
	ArtistId INTEGER,
	FOREIGN KEY (ArtistId) REFERENCES artists(ArtistId)
);

CREATE TABLE IF NOT EXISTS artists (
	ArtistId INTEGER,
	Name NVARCHAR(120)
);

CREATE TABLE IF NOT EXISTS customers (
	CustomerId INTEGER,
	FirstName NVARCHAR(40),
	LastName NVARCHAR(20),
	Company NVARCHAR(80),
	Address NVARCHAR(70),
	City NVARCHAR(40),
	State NVARCHAR(40),
	Country NVARCHAR(40),
	PostalCode NVARCHAR(10),
	Phone NVARCHAR(24),
	Fax NVARCHAR(24),
	Email NVARCHAR(60),
	SupportRepId INTEGER,
	FOREIGN KEY (FirstName) REFERENCES employees(FirstName)
);

CREATE TABLE IF NOT EXISTS employees (
	EmployeeId INTEGER,
	LastName NVARCHAR(20),
	FirstName NVARCHAR(20),
	Title NVARCHAR(30),
	ReportsTo INTEGER,
	BirthDate DATETIME,
	HireDate DATETIME,
	Address NVARCHAR(70),
	City NVARCHAR(40),
	State NVARCHAR(40),
	Country NVARCHAR(40),
	PostalCode NVARCHAR(10),
	Phone NVARCHAR(24),
	Fax NVARCHAR(24),
	Email NVARCHAR(60)
);

CREATE TABLE IF NOT EXISTS genres (
	GenreId INTEGER,
	Name NVARCHAR(120)
);

CREATE TABLE IF NOT EXISTS invoices (
	InvoiceId INTEGER,
	CustomerId INTEGER,
	InvoiceDate DATETIME,
	BillingAddress NVARCHAR(70),
	BillingCity NVARCHAR(40),
	BillingState NVARCHAR(40),
	BillingCountry NVARCHAR(40),
	BillingPostalCode NVARCHAR(10),
	Total NUMERIC(10,2),
	FOREIGN KEY (CustomerId) REFERENCES customers(CustomerId)
);

CREATE TABLE IF NOT EXISTS invoice_items (
	InvoiceLineId INTEGER,
	InvoiceId INTEGER,
	TrackId INTEGER,
	UnitPrice NUMERIC(10,2),
	Quantity INTEGER,
	FOREIGN KEY (InvoiceId) REFERENCES invoices(InvoiceId),
	FOREIGN KEY (TrackId) REFERENCES tracks(TrackId)
);

CREATE TABLE IF NOT EXISTS media_types (
	MediaTypeId INTEGER,
	Name NVARCHAR(120)
);

CREATE TABLE IF NOT EXISTS playlists (
	PlaylistId INTEGER,
	Name NVARCHAR(120)
);

CREATE TABLE IF NOT EXISTS playlist_track (
	PlaylistId INTEGER,
	TrackId INTEGER,
	FOREIGN KEY (TrackId) REFERENCES tracks(TrackId),
	FOREIGN KEY (PlaylistId) REFERENCES playlists(PlaylistId)
);

CREATE TABLE IF NOT EXISTS tracks (
	TrackId INTEGER,
	Name NVARCHAR(200),
	AlbumId INTEGER,
	MediaTypeId INTEGER,
	GenreId INTEGER,
	Composer NVARCHAR(220),
	Milliseconds INTEGER,
	Bytes INTEGER,
	UnitPrice NUMERIC(10,2),
	FOREIGN KEY (AlbumId) REFERENCES albums(AlbumId),
	FOREIGN KEY (MediaTypeId) REFERENCES media_types(MediaTypeId),
	FOREIGN KEY (GenreId) REFERENCES genres(GenreId)
);


namespace Domain.Entities;
public class SpecialDay
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public DateOnly Date { get; set; }
    public string? Description { get; set; }
}

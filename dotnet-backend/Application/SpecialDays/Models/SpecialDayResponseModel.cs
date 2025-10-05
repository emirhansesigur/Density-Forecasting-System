namespace Application.SpecialDays.Models;
public class SpecialDayResponseModel
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public DateOnly Date { get; set; }
    public string? Description { get; set; }
}
